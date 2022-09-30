
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
        sql = "SELECT * from face_db.user"
        result_count = cursor.execute(sql)
        user = cursor.fetchall()
        connection.close()
        return user

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

def del_person():
    return True
def add_person(name, info, reg):
    connection = conn()
    with connection.cursor() as cursor:
        sql = "INSERT INTO `face_db`.`person` (`name`, `information`, `is_recog`) VALUES ('"+name+"', '"+info+"', '"+reg+"');"
        try:
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return True
        except:
            ...
    return False
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
def add_image(idp, link, imv):
    connection = conn()
    with connection.cursor() as cursor:
        sql = "INSERT INTO `face_db`.`image` (`id_person`, `link`, `index_milvus`) VALUES ('"+idp+"', '"+link+"', '"+imv+"');"
        try:
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return True
        except:
            ...
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
def conn():
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='face_db')
    return connection


    