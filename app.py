from email import message
from flask_ngrok import run_with_ngrok
import cv2
from tkinter import image_names
from flask import jsonify
from multiprocessing import connection
from sqlite3 import connect
from unittest import result
from flask import Flask, Response, render_template, redirect, url_for, request, make_response
from connector_to_mySQL import add_cams, add_image, add_person_, add_user, change_pass, change_status_, check_login, check_username, conn, create_user_, delete_object_, delete_user, find_by_ID, get_all_User, get_all_cam, get_all_img_obj, get_all_location, get_all_persons, get_infor_obj, get_link, get_main_img, get_max_id, get_noti_5_sec, get_noti_of_object_
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from functools import wraps
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
 
app.config['UPLOAD_PATH'] = 'static/image'

def find_camera(id):
    # cameras = ["rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4"]*28
    cameras = ['0'] * 28
    return cameras[int(id)], len(cameras)
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
#  for webcam use zero(0)
 

def gen_frames(camera_id):
    camera_id=get_link(camera_id)
    print(camera_id)

    print(camera_id)
    cap=  cv2.VideoCapture(camera_id)
    print(camera_id)
    while True:
        # for cap in caps:
        # # Capture frame-by-frame
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed/<string:id>/', methods=["GET"])
def video_feed(id):
   
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frame(url):

    cap=  cv2.VideoCapture(url)
    
    while True:
        # for cap in caps:
        # # Capture frame-by-frame
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/cam-test', methods=["GET"])
def video_feed_test():
    url = request.cookies.get('rtsp')
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(url),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
 
 
@app.route('/')
def welcome():
    return redirect('/login')
 
 
@app.route('/index')
def home():
	_, num_of_cam = find_camera(0)
	i1 = int(num_of_cam/4)
	dict_loc = {}
	for i in get_all_location():
		dict_loc[i[0]] = []
	for i in get_all_cam():
		dict_loc[i[3]].append(i)
	i2 = num_of_cam % 4 if num_of_cam % 4 != 0 else 4
	
	return render_template('index-2.html', i1 = i1, i2=i2, dict_loc = dict_loc)
 
@app.route('/object')
def object():
	persons = get_all_persons()

	return render_template('object-management.html', persons=persons)
@app.route('/is-recog')
def is_recog():
	persons = get_all_persons()
	p = []
	for person in persons:

		p1 = []
		for i in person:
			
			p1.append(str(i))
		p.append(p1)
		
	return jsonify({'message': p})

@app.route('/change-status', methods=['POST'])
def change_status():
	data = request.get_json()
	change_status_(data["id"], data["change"])
	return jsonify({'message':"Successful!!!"})
@app.route('/camera')
def camera():
    return render_template('camera-management.html')
@app.route('/add-cam', methods=["POST"])
def add_cam():
	data = request.get_json()

	print(data)
	if add_cams(data["name"], data["link"], data["locate"]):
		return jsonify({'message': 'success'})
	return jsonify({'message': 'ERROR: Link đã tồn tại'})
	
@app.route('/add-person', methods=["POST"])
def add_person():
	data = request.get_json()

	print(data)
	if add_person_(data["name"], data["info"]):
		k = get_max_id()
		return jsonify({'message': 'success', 'id': k})
	return jsonify({'message': 'ERROR: Link đã tồn tại'})

@app.route('/delete-object', methods=["DELETE"])
def delete_object():
	data = request.get_json()
	print(data["id"])
	
	if delete_object_(data["id"]):
		return jsonify({'message': 'success'})
	return jsonify({'message': 'ERROR: Lỗi server!'})


@app.route('/account-management')
def acc_mng():
	
	
	users = get_all_User()
	
	return render_template('acc-mng.html', users = users)
@app.route('/check-camera', methods=['VIEW'])
def check_camera():
    return render_template('camera-management.html')

@app.route('/update-object', methods=['GET', 'POST']) 
def createObject():
	return render_template('object-update.html')

@app.route('/uploader/<int:id>', methods = ['GET', 'POST'])
def upload_file(id):
	arr = []
	if request.method == 'POST':
		
		for f in request.files.getlist("file[]"):
			arr.append(app.config['UPLOAD_PATH']+ '/'+ secure_filename(f.filename))
			f.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(f.filename)))

	
	print(add_image(id, arr))
	main = get_main_img(id)
	all = get_all_img_obj(id)
	infor = get_infor_obj(id)
	info = infor[0][2]
	name = infor[0][1]
	rows = int(len(all)/3-1)
	print(rows)
	lastrow = len(all)%3
	if lastrow == 0: lastrow = 3
	return render_template('object-update.html', main=main, all = all, id = id, info=info, name=name, rows = rows, lastrow = lastrow)


@app.route('/get-all-image/<int:id>', methods = ['GET'])
def upload_figetle(id):
	data = {
		'main': get_main_img(id),
		'all': get_all_img_obj(id)
	}
	return jsonify(data)


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        if not check_login(request.form['username'],request.form['password']):
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    
    return render_template('login.html', error=error)


@app.route('/change-pass', methods=["POST"])
def change_pass_route():
	data = request.get_json()
	
	
	if change_pass(data["name"], data["pass"], data["role"]):
		return jsonify({'message': 'success'})
	return jsonify({'message': 'Lỗi server'})

@app.route('/del-user', methods=["DELETE"])
def del_user():
	data = request.get_json()
	
	
	if delete_user(data["user"]):
		return jsonify({'message': 'success'})
	return jsonify({'message': 'Lỗi server'})

@app.route('/create-user', methods=["POST"])
def create_user_route():
	data = request.get_json()
	
	
	if create_user_(data["user"], data["pass"], data["role"]):
		return jsonify({'message': 'success'})
	return jsonify({'message': 'Lỗi server'})

# token JWT:
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		# jwt is passed in the request header
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
		# return 401 if token is not passed
		if not token:
			return jsonify({'message' : 'Token is missing !!'}), 401

		try:
			# decoding the payload to fetch the stored details
			data = jwt.decode(token, app.config['SECRET_KEY'])
			current_user = find_by_ID(data['public_id']) 
			if current_user == None: 
				raise Exception("Have no user with provided ID")
		except:
			return jsonify({
				'message' : 'Token is invalid !!'
			}), 401
		# returns the current logged in users contex to the routes
		return f(current_user, *args, **kwargs)

	return decorated

# Get list users:

@app.route('/user', methods =['GET'])
def get_all_users():
	# querying the database
	# for all the entries in it
	users = get_all_User()
	# converting the query objects
	# to list of jsons
	output = []
	for user in users:
		# appending the user data json
		# to the response list
		output.append({
			'public_id': user[0],
			'name' : user[1],
			'role': 'admin' if user[3] else 'user',
			'create_date' : user[4]
		})

	return jsonify({'users': output})

@app.route('/create-user', methods =['POST'])
@token_required
def create_user():
	# creates a dictionary of the form data
	data = request.form

	# gets name, email and password
	name= data.get('name')
	password = data.get('password')
	role = data.get('role')
	# checking for existing user
	user = check_username(name)
	if not user:
		
		res = add_user(name, password, role )
		if res == True:
			return make_response('Successfully registered.', 201)
		else:
			raise Exception('user exists')
	else:
		# returns 202 if user already exists
		return make_response('User already exists. Please Log in.', 202)

@app.route('/noti-5-secs', methods =['GET'])
def get_noti_5_secs():
	# querying the database
	# for all the entries in it
	users = get_noti_5_sec()
	# converting the query objects
	# to list of jsons
	output = []
	for user in users:
		# appending the user data json
		# to the response list
		output.append({
			'id': user[0],
			'time' : str(user[1]),
			'person_name': user[2],
			'score' : user[3],
			'cam' : user[4],
			'location' :user[5]
		})

	return jsonify({'notification': output})

@app.route('/get-noti-of-object', methods =['POST'])
def get_noti_of_object():
	id = request.get_json()
	
	# querying the database
	# for all the entries in it
	users = get_noti_of_object_(id["id"])
	# converting the query objects
	# to list of jsons
	print(users)
	output = []
	for user in users:
		# appending the user data json
		# to the response list
		output.append({
			'id': user[0],
			'time' : str(user[1]),
			
			'score' : user[2],
			'cam' : user[3],
			'location' :user[4]
		})
	print(output)
	return jsonify({'notification': output})


if __name__ == '__main__':
    app.run(host='localhost', port=5000)