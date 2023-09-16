from sqlalchemy import text
from sql_connection import conn
import random

def sql(string):
    return conn.execute(text(string))

def sql_token_exists_in_db(token):
    result = sql(f"select EXISTS(select token from session where token = '{token}')").scalar()
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
    sql(f"update session set token = '{token}' where user_id = {id_user}")

def sql_token_to_user(token):
    id = sql(f"select user_id from session where token = '{token}'").scalar()
    name = sql(f"select name from users where id = {id}").scalar()
    return name

def sql_change_image_location(filename_from, filename_to):
    sql(f"update pictures set path = '{filename_to}' where path = '{filename_from}'")

def sql_remove_image_location(filename):
    sql(f"delete from pictures where path = '{filename}'")

def sql_change_avatar(username, filename):
    id_user = sql(f"select id from users where name = '{username}'").scalar()
    sql(f"update pictures set ava_path = '{filename}' where user_id = '{id_user}'")

def sql_get_avatar(username):
    id_user = sql(f"select id from users where name = '{username}'").scalar()
    result = sql(f"select ava_path from avatar where user_id = '{id_user}'").scalar()
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