from sqlalchemy import text
from sql_connection import conn
import random



def sql(string):
    try:
        return conn.execute(text(string))
    except Exception as e:
        print(f"Can't do that\n error discription: {e}")

def sql_token_exists_in_db(token):
    result = 0
    try:
        result = sql(f"select EXISTS(select token from session where token = '{token}')").scalar()
    except:
        result = 0
    return int(result)


def sql_username_exists(username):
    result = sql(f"select EXISTS(select name from users where name = '{username}')").scalar()
    return int(result) # ok, 10/10 very good

def sql_get_user_password_hash(username):
    result = sql(f"select password from users where name = '{username}'").scalar()
    return result

def sql_add_user(username, password):
    id = sql(f"select count(id) from users").scalar()
    sql(f"insert into users values({id}, '{username}', '{password}', 0, NULL,  {random.choice(range(100000,999999))})")
    sql(f"insert into session values(NULL, {id})")
    sql(f"insert into avatar values(NULL, {id})")

def sql_set_user_auth_status(username, status):
    sql(f"update users set accepted_status = {status} where name = '{username}'")
    

def sql_get_all_user_pictures_with_pattern(username, pattern):
    pattern = str(pattern)
    parsed = pattern.replace('*', '%')
    result = sql(f"select p.path from pictures p join users u on (p.user_id = u.id) where u.name = '{username}' and p.path like '{parsed}'").fetchall()
    return result

def sql_post_image_location(username, file_location):
    id_user = sql(f"select id from users where name = '{username}'").scalar()
    sql(f"insert into pictures values({id_user}, '{file_location}')")


def sql_get_user_telegram_authkey(username):
    result = sql(f"select telegram_code from users where name = '{username}'").scalar()
    return result

def sql_change_auth_token(username, token):
    id_user = sql(f"select id from users where name = '{username}'").scalar()
    # sql(f"update session set token = '{token}' where user_id = {id_user}")
    sql(f"insert into session values ('{token}', {id_user})")

def sql_token_to_user(token):
    try:
        id = sql(f"select user_id from session where token = '{token}'").scalar()
        name = sql(f"select name from users where id = {id}").scalar()
        return name
    except Exception as e:
        print("Failed to cum", e)

def sql_token_to_user_id(token):
    try:
        id = sql(f"select user_id from session where token = '{token}'").scalar()
        return id
    except Exception as e:
        print("Failed to cum 2", e)

def sql_change_image_location(user_id, filename_from, filename_to):
    sql(f"update pictures set path = '{filename_to}' where path = '{filename_from}' and user_id = '{user_id}'")

###
def sql_does_image_exist(path):
    result = sql(f"select EXISTS(select path from pictures where path = '{path}')")
    return result

def sql_remove_image_location(user_id, filename):
    sql(f"delete from pictures where path = '{filename}' and user_id = '{user_id}'")

def sql_remove_image_by_pattern(user_id, pat):
    sql(f"delete from pictures where path like '{pat}' and user_id = '{user_id}'")

def sql_change_avatar(username, filename):
    id_user = sql(f"select id from users where name = '{username}'").scalar()
    sql(f"update avatar set ava_path = '{filename}' where user_id = {id_user}")

def sql_get_avatar(username):
    result = 0
    try:
        id_user = sql(f"select id from users where name = '{username}'").scalar()
        result = sql(f"select ava_path from avatar where user_id = '{id_user}'").scalar()
    except:
        result = None
    return result

def sql_delete_token(token):
    sql(f"delete from session where token = '{token}'")


def sql_get_user_auth_status(username):
    result = sql(f"select accepted_status from users where name = '{username}'")
    return result

def print_table(table_name):
    '''
    Can out tables:
    users
    pictures
    session
    avatar
    '''
    print( sql(f"select * from {table_name}").fetchall())
    print("Len:",len(sql(f"select * from {table_name}").fetchall()))