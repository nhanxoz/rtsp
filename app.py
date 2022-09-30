from email import message
from flask_ngrok import run_with_ngrok
import cv2
from tkinter import image_names
from flask import jsonify
from multiprocessing import connection
from sqlite3 import connect
from unittest import result
from flask import Flask, Response, render_template, redirect, url_for, request, make_response
from connector_to_mySQL import add_user, check_login, check_username, conn, find_by_ID, get_all_User
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from functools import wraps
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
 


 
@app.route('/')
def welcome():
    return redirect('/login')
 
 
@app.route('/index')
def home():
    return render_template('index-2.html')
 
@app.route('/object')
def object():
    return render_template('object-management.html')


@app.route('/camera')
def camera():
    return render_template('camera-management.html')

@app.route('/check-camera', methods=['VIEW'])
def check_camera():
    return render_template('camera-management.html')

@app.route('/update-object', methods=['GET', 'POST']) 
def createObject():
	return render_template('object-update.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

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
@token_required
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



if __name__ == '__main__':
    app.run(host='localhost', port=5000)