from sqlalchemy import text
from sql_connection import conn
import random

def sql_token_exists_in_db(token):
    result = conn.execute(text(f"select EXISTS(select token from session where token = '{token}')")).scalar()
    return int(result)# ok, 10/10 very good


def sql_username_exists(username):
    result = conn.execute(text(f"select EXISTS(select name from users where name = '{username}')")).scalar()
    return int(result)# ok, 10/10 very good

def sql_get_user_password_hash(username):
    result = conn.execute(text(f"select password from users where name = '{username}'")).scalar()
    return result

def sql_add_user(username, password):
    id = conn.execute(text(f"select count(id) from users")).scalar()
    conn.execute(text(f"insert into users values({id}, '{username}', '{password}', 0, NULL,  {random.choice(range(100000,999999))})"))
    conn.execute(text(f"insert into session values(NULL, {id})"))
    conn.execute(text(f"insert into avatar values(NULL, {id})"))

def sql_set_user_auth_status(username, status):
    conn.execute(text(f"update users set accepted_status = {status} where name = '{username}'"))
    

def sql_get_all_user_pictures_with_pattern(username, pattern):
    parsed = pattern.replace('*', '%')
    result = conn.execute(text(f"select p.path from pictures p join users u on (p.user_id = u.id) where u.name = '{username}' and p.path like '{parsed}'")).fetchall()
    return result

def sql_post_image_location(username, file_location):
    id_user = conn.execute(text(f"select id from users where name = '{username}'")).scalar()
    conn.execute(text(f"insert into pictures values({id_user}, '{file_location}')"))


def sql_get_user_telegram_authkey(username):
    result = conn.execute(text(f"select telegram_code from users where name = '{username}'")).scalar()
    return result

def sql_change_auth_token(username, token):
    id_user = conn.execute(text(f"select id from users where name = '{username}'")).scalar()
    conn.execute(text(f"update session set token = '{token}' where user_id = {id_user}"))

def sql_token_to_user(token):
    id = conn.execute(text(f"select user_id from session where token = '{token}'")).scalar()
    name = conn.execute(text(f"select name from users where id = {id}")).scalar()
    return name

def sql_change_image_location(filename_from, filename_to):
    conn.execute(text(f"update pictures set path = '{filename_to}' where path = '{filename_from}'"))

def sql_remove_image_location(filename):
    conn.execute(text(f"delete from pictures where path = '{filename}'"))

def sql_change_avatar(username, filename):
    id_user = conn.execute(text(f"select id from users where name = '{username}'")).scalar()
    conn.execute(text(f"update pictures set ava_path = '{filename}' where user_id = '{id_user}'"))


    








