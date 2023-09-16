from sqlalchemy import text
from sql_connection import conn

# test import
from sql_test_data import albom_name, names, generate_password, generate_path, generate_tg_id
import random

#funt for Vasyan
from sql_funct import *

def main_sql_func():
    #indexes
    index1 = "create unique index if not exists fast_indx on pictures (path)"
    index2 = "create unique index if not exists avatarka_indx on avatar (ava_path)"
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
    list_index = [index1, index2]
    try:
        select_table(select)
        print("Database exisits")
    except Exception as e:
        print(f"Err: database not found, Creating new...\n Discript error: {e}")
        sql_execute_list(list_create)
        sql_execute_list(list_index)
        
    #insert_tables(10)
    #
    #print("BASE:")
    #print_table('users')
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
    #sql_add_user('Misha', 'VASYA-petya')
    #sql_set_user_auth_status('Misa', 1)
    #sql_change_auth_token('Misha', 'XXXvideos')
    #sql_delete_token('XXXvideos')
    #insert_tables(5)
    #print_table('users')

    #tests
    #select_all(select, select2)
    #drop_tables(delete, delete2)





def sql_execute_list(list):
    for i in list:
        sql(i)

# it is for testing 
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
    result = conn.execute(text(select)).fetchall()
    print(result)
    return result

main_sql_func()