
import pymysql

# USER
def check_login(user_name,password):
    connection= conn()
    with connection.cursor() as cursor:
        sql = "SELECT password FROM face_db.user where username = '"+ user_name+"';"
        result_count = cursor.execute(sql)
        password_get = cursor.fetchone()
        if(password_get[0] == password):
            connection.close()
            return True
        connection.close()
    return False

def find_by_ID(id):
    connection = conn()
    with connection.cursor() as cursor:
        sql = "SELECT username, role FROM face_db.user where id = '"+ id+"';"
        result_count = cursor.execute(sql)
        user = cursor.fetchone()
        connection.close()
        return user

def get_all_User():
    connection = conn()
    with connection.cursor() as cursor:
        sql = "SELECT id, username, char_length(password), role FROM face_db.user;"
        result_count = cursor.execute(sql)
        user = cursor.fetchall()
        connection.close()
        return user
def get_all_location():
    connection = conn()
    with connection.cursor() as cursor:
        sql = "select distinct(loaction) from face_db.camera;"
        result_count = cursor.execute(sql)
        loc = cursor.fetchall()
        connection.close()
        return loc
def get_all_cam():
    connection = conn()
    with connection.cursor() as cursor:
        sql = "select * from face_db.camera;"
        result_count = cursor.execute(sql)
        cam = cursor.fetchall()
        connection.close()
        return cam
def get_link(c):
    connection = conn()
    with connection.cursor() as cursor:
        sql = "select link from face_db.camera where id = " + str(c)
        print(sql)
        result_count = cursor.execute(sql)
        cam = cursor.fetchall()
        connection.close()
        print(cam[0][0])
        return cam[0][0]
def get_noti_5_sec():
    connection = conn()
    with connection.cursor() as cursor:
        sql = "SELECT notification.id, time, person.name, score, camera.name, loaction  FROM face_db.notification join face_db.person on notification.id_person = person.id join face_db.camera on camera.id = notification.id_camera"
        result_count = cursor.execute(sql)
        cam = cursor.fetchall()
        connection.close()
        return cam

def get_noti_of_object_(id):
    connection = conn()
    with connection.cursor() as cursor:
        sql = "SELECT notification.id, time, score, camera.name, loaction  FROM face_db.notification join face_db.person on notification.id_person = person.id join face_db.camera on camera.id = notification.id_camera where person.id ='" +id+"'"
        result_count = cursor.execute(sql)
        cam = cursor.fetchall()
        connection.close()
        return cam

def check_username(username):
    connection = conn()
    with connection.cursor() as cursor:
        sql = "SELECT id from face_db.user where username= '" + username +"'"
        result_count = cursor.execute(sql)
        return result_count

def add_user(username, password, role):
    connection = conn()
    with connection.cursor() as cursor:
        try:
            sql = "INSERT INTO `face_db`.`user` (`username`, `password`, `role`) VALUES ('"+username+"', '"+password+"', '"+role+"')"
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return True
        except:
            return False

# PERSON function
def get_all_persons():
    connection = conn()
    with connection.cursor() as cursor:
        sql = "SELECT * from face_db.person"
        result_count = cursor.execute(sql)
        ps = cursor.fetchall()
        connection.close()
        return ps

def change_status_(id, value):
    connection = conn()
    value = str(1 if value else 0)
    with connection.cursor() as cursor:
        try:
            sql = "UPDATE `face_db`.`person` SET `is_recog` = '"+ value +"' WHERE (`id` = '"+id+"');"
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return True
        except:
            return False
def delete_object_(c):
    connection = conn()
    c = str(c)
    with connection.cursor() as cursor:
        try:
            sql = "DELETE FROM `face_db`.`person` WHERE (`id` = '"+c+"');"
            print(sql)
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return True
        except:
            return False
    return True
def add_person_(name, info):
#     INSERT INTO `face_db`.`person` (`name`, `information`, `is_recog`, `main_image`) VALUES ('2', '2', '1', '/static/image/jisoo.png');
# INSERT INTO `face_db`.`person` (`name`, `information`, `is_recog`, `main_image`) VALUES ('3', '3', '1', '/static/image/jisoo.png');
# INSERT INTO `face_db`.`person` (`name`, `information`, `is_recog`, `main_image`) VALUES ('4', '4', '1', '/static/image/jisoo.png');
# INSERT INTO `face_db`.`person` (`name`, `information`, `is_recog`, `main_image`) VALUES ('5', '5', '1', '/static/image/jisoo.png');
# INSERT INTO `face_db`.`person` (`name`, `information`, `is_recog`, `main_image`) VALUES ('6', '6', '1', '/static/image/jisoo.png');

    connection = conn()
    with connection.cursor() as cursor:
        sql = "INSERT INTO `face_db`.`person` (`name`, `information`, `is_recog`) VALUES ('"+name+"', '"+info+"', '1');"
        try:
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return True
        except:
            ...
    return False

# select MAX(id) from face_db.person;
def get_max_id():
    connection = conn()
    with connection.cursor() as cursor:
        sql = "select MAX(id) from face_db.person;"
        result_count = cursor.execute(sql)
        ps = cursor.fetchall()
        connection.close()
        return ps[0][0]


def update_person(id, name, info, reg):
    connection = conn()
    with connection.cursor() as cursor:
        sql = "UPDATE `face_db`.`person` SET `name` = '"+name+"', `information` = '"+info+"', `is_recog` = '"+reg+"' WHERE (`id` = '"+id+"');"
        try:
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return True
        except:
            ...
    return False
#IMAGE function
def get_all_images():
    connection = conn()
    with connection.cursor() as cursor:
        sql = "SELECT * from face_db.image"
        result_count = cursor.execute(sql)
        ps = cursor.fetchall()
        connection.close()
        return ps

def del_image(id):
    connection = conn()
    with connection.cursor() as cursor:
        sql = "delete from face_db.image where id =" +id
        try:
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return True
        except:
            ...
    return False

def get_main_img(id):
    id = str(id)
    connection = conn()
    with connection.cursor() as cursor:
        sql = "SELECT main_image from face_db.person where id="+id
        
        result_count = cursor.execute(sql)
        ps = cursor.fetchall()
        connection.close()
    return ps[0][0]

def get_infor_obj(id):
    id=str(id)
    connection = conn()
    with connection.cursor() as cursor:
        sql = "SELECT * from face_db.person where id="+id
        
        result_count = cursor.execute(sql)
        ps = cursor.fetchall()
        connection.close()
    return ps




def get_all_img_obj(id):
    id = str(id)
    connection = conn()
    with connection.cursor() as cursor:
        sql = "SELECT link from face_db.image where id_person="+id
        
        result_count = cursor.execute(sql)
        ps = cursor.fetchall()
        connection.close()
    return ps
def check_main_img(idp, arrlink):
    connection = conn()
    with connection.cursor() as cursor:
        sql = "SELECT main_image from face_db.person where id="+idp
        
        result_count = cursor.execute(sql)
        ps = cursor.fetchall()
        connection.close()
    if ps[0][0] == None:
        connection = conn()
        with connection.cursor() as cursor:
            sql = "UPDATE `face_db`.`person` SET `main_image` = '"+arrlink[0]+"' WHERE (`id` = '"+idp+"');"
            
            cursor.execute(sql)
            connection.commit()
            connection.close()
    return ps
def add_image(idp, arrlink):
    try:
        idp = str(idp)
        check_main_img(idp, arrlink)
        for link in arrlink:
            connection = conn()
            with connection.cursor() as cursor:
                sql = "INSERT INTO `face_db`.`image` (`id_person`, `link`) VALUES ('"+idp+"', '"+link+"');"
                
                cursor.execute(sql)
                connection.commit()
                connection.close()
        return True
    except:
        return False
                
    
def update_image(id, idp, link, imv):
    connection = conn()
    with connection.cursor() as cursor:
        sql = "UPDATE `face_db`.`image` SET `link` = '"+link+"', `index_milvus` = '"+imv+"', `id_person` = '"+idp+"' WHERE (`id` = '"+id+"');"
        try:
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return True
        except:
            ...
    return False


# Cam function

def check_exists_cam(name, link, location):
    connection = conn()
    with connection.cursor() as cursor:
        sql = "select * from `face_db`.`camera` where link = '"+link+"';"

        
        try:
            result_count = cursor.execute(sql)
            print(result_count)
            if result_count != 0:
                return False
            connection.close()
            return True
        except:
            ...
    return False

def add_cams(name, link, location):
    if check_exists_cam(name, link, location)==False:
        return False
    connection = conn()
    with connection.cursor() as cursor:
        sql = "INSERT INTO `face_db`.`camera` (`name`, `link`, `loaction`, `is_recog`) VALUES ('"+name+"', '"+link+"', '"+location+"', '2');"
        try:
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return True
        except:
            ...
    return False

def change_pass(name, pw, role):
    # UPDATE `face_db`.`user` SET `password` = '12341234', `role` = '1234' WHERE (`id` = '3');
    connection = conn()
    role = 1 if role else 0
    with connection.cursor() as cursor:
        sql = "UPDATE `face_db`.`user` SET `password` = '"+pw+"', `role` = '"+str(role)+"' WHERE (`username` = '"+name+"');"
        print(sql)
        try:
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return True
        except:
            ...
    return False

def delete_user(name):
    # DELETE FROM `face_db`.`user` WHERE (`id` = '5');
    connection = conn()
    
    with connection.cursor() as cursor:
        sql = "DELETE FROM `face_db`.`user` WHERE (`username` = '"+name+"');"
        print(sql)
        try:
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return True
        except:
            ...
    return False


def create_user_(name, pw, role):
    # INSERT INTO `face_db`.`user` (`username`, `password`, `role`) VALUES ('4', '4', '4');
    connection = conn()
    role = str(1 if role else 0)
    with connection.cursor() as cursor:
        sql = "INSERT INTO `face_db`.`user` (`username`, `password`, `role`) VALUES ('"+name+"', '"+pw+"', '"+role+"');"
        print(sql)
        try:
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return True
        except:
            ...
    return False
def conn():
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='face_db')
    return connection


    