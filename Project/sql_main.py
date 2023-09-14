from sqlalchemy import create_engine
from sqlalchemy import text

# test import
from sql_test_data import albom_name, names, generate_password, generate_path
import random

def main_sql_func():
    engine = create_engine('postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/postgres')
    print(engine)
    conn = engine.connect()
    #selects
    select = "select * from users"
    select2 = "select * from pictures"
    #create table
    create_query = "create table users (id int, name varchar(60), password varchar(60))"
    create_query2 = "create table pictures (id int, path text, albom varchar(60))"
    #dml

    #delete
    delete = "drop table users"
    delete2 = "drop table pictures"
    create_tables(conn, create_query, create_query2)
    # insert_tables(conn, 100)
    select_all(conn, select, select2)
    # drop_tables()
    return engine


def create_tables(conn, create_query, create_query2):
    conn.execute(text(create_query))
    conn.execute(text(create_query2))

def insert_tables(conn, end_range): 
    for i in range(0, end_range):
        insert_user = f"insert into users values({i},'{random.choice(names)}', '{generate_password(20)}')"
        insert_pictures = f"insert into pictures values({random.choice([i for i in range(0, end_range)])}, '{generate_path(20)}', '{random.choice(albom_name)}')"
        conn.execute(text(insert_user))
        conn.execute(text(insert_pictures))

def select_all(conn, select, select2):
    result = conn.execute(text(select)).fetchall()
    print(result)
    result2 = conn.execute(text(select2)).fetchall()
    print(result2)


def drop_tables(conn):
    conn.execute(text(delete))
    conn.execute(text(delete2))