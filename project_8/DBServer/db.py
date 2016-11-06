#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Database Module'''

import sqlite3

def init_database():

    '''Initialize database'''

    conn = sqlite3.connect('database.db')
    conn.execute("create table if not exists user(email text primary key not null, password text not null, token text)")
    conn.commit()
    print("Connect to database successful!")
    return conn

def valid_user(conn, email, password):

    '''Valid user'''

    cursor = conn.execute("select count(*) from user where email=? and password=?", (email, password,))
    return cursor.fetchone()[0]

def insert_user(conn, email, password):

    '''Insert user'''

    try:
        conn.execute("insert into user (email, password) values (?, ?)", (email, password,))
        conn.commit()
        return True
    except:
        return False

def add_token(conn, email, token):

    '''Add a token to a user'''

    conn.execute("update user set token=? where email=?", (token, email,))
    conn.commit()
    return conn.total_changes

def valid_token(conn, token):

    '''Valid token'''
    
    cursor = conn.execute("select count(*) from user where token=?", (token,))
    return cursor.fetchone()[0]