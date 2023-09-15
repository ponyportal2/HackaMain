from sqlalchemy import text
from sql_connection import conn

# test import
from sql_test_data import albom_name, names, generate_password, generate_path, generate_tg_id
import random

#funt for Vasyan
from sql_funct import *
# str = 'aygsjf.png'
# res = str.split("."); 

def main_sql_func():
    #selects
    select = "select * from users"
    select2 = "select * from pictures"
    #create table
    create_query = "create table users (id int, name varchar(60), password varchar(60), accepted_status int, telegram_id int, telegram_code int)" # password is stored as a hash !!!!!!
    create_query2 = "create table pictures (user_id int, path text)"
    create_query3 = "create table session (token varchar(255), user_id int)"
    create_query4 = "create table avatar (ava_path text, user_id int)"
    # add a query in there to create a table for the data
    list_create = [create_query, create_query2, create_query3, create_query4]
    #dml
    #tests
    delete = "DROP TABLE users"
    delete2 = "DROP TABLE pictures"
    try: 
        select_table(select)
    except Exception as e:
        create_tables(list_create)
        
    #insert_tables(1000)
    #print(sql_username_exists('John'))
    #print(sql_username_exists('LL'))
    #print(sql_username_exists('Psychokid'))
    #print(f"Password_hash for psychokid: ", sql_get_user_password_hash('Psychokid'))
    #sql_add_user('Misha', 'VASYA-petya')
    #print(sql_username_exists('Misha'))
    #print(f"Password_hash for Misha: ", sql_get_user_password_hash('Misha'))
    #sql_set_user_auth_status('Misa', 1)
    #print(sql_get_user_telegram_authkey("Misha"))
    #sql_change_auth_token('Misha', 'XXXvideos')
    #print(sql_token_to_user('XXXvideos'))
    #print(sql_get_all_user_pictures_with_pattern("John", "u*"))

    #print(sql_get_all_user_album_names('John'))

    #tests

    #select_all(select, select2)
    #drop_tables(delete, delete2)
    #return engine




def create_tables(list):
    for i in list:
        conn.execute(text(i))

def insert_tables(end_range): 
    for i in range(0, end_range):
        insert_user = f"insert into users values({i},'{random.choice(names)}', '{generate_password(20)}', 1, {generate_tg_id(12)}, {random.choice(range(100000,999999))})"
        conn.execute(text(insert_user))
        if i > 2:
            insert_pictures = f"insert into pictures values({random.choice([i for i in range(0, i)])}, '{generate_path(20)}')"
            insert_sessions = f"insert into session values('{generate_password(40)}', {random.choice([i for i in range(0, i)])})"
            conn.execute(text(insert_pictures))
            conn.execute(text(insert_sessions))
        
        
        

def select_table(select):
    result = conn.execute(text(select)).scalar()
    print(result)
    return result


def drop_tables(delete, delete2):
    conn.execute(text(delete))
    conn.execute(text(delete2))


main_sql_func()