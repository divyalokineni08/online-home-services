import json
import sqlite3
from datetime import datetime

from utils import send_mail

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    db = sqlite3.connect('db.sqlite3')
    db.row_factory = dict_factory
    cursor = db.cursor()
    cursor.execute("create table if not exists ub_emp (id integer primary key, first_name text, last_name text, password text, email text, mobileno text, language text, gender text)")
    cursor.execute("""
        create table if not exists customer (id integer primary key, first_name text, last_name text, password text, email text, mobileno text, address text, state text, city text, zip text, country text, gender text)
                   """)
    cursor.execute("""
        create table if not exists service (id integer primary key, service_type text, service_data text, service_time text, language text, status text default "pending", customer_id integer, emp_id integer)
                   """)
    def save(): return db.commit()
    def close(): return db.close()
    return cursor, save, close


def create_customer(first_name, last_name, password, mail, mobile_no, address, state, city, zip ,country, gender):
    cursor, save, close = get_db()
    cursor.execute("""
            insert into customer (first_name, last_name, password, email, mobileno, address, state, city, zip, country, gender) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   """, (first_name, last_name, password, mail, mobile_no, address, state, city, zip ,country, gender))
    save()
    close()



def create_emp(first_name, last_name, password, mail, mobile_no, language,gender):
    cursor, save, close = get_db()
    cursor.execute("""
            insert into ub_emp (first_name, last_name, password, email, mobileno, language,gender)
            values (?, ?, ?, ?, ?, ?,?)
                   """, (first_name, last_name, password, mail, mobile_no, language,gender))
    save()
    close()

def login_customer(mail, password):
    cursor, _, close = get_db()
    user = cursor.execute("""
        select * from customer where email =? and password =?
                   """, (mail, password)).fetchone()
    close()
    return user

def login_emp(mail, password):
    cursor, _, close = get_db()
    user = cursor.execute("""
        select * from ub_emp where email =? and password =?
                   """, (mail, password)).fetchone()
    print("emp login")
    close()
    return user

def book_servcie(service_type, service_data, service_time, langauge, customer_id):
    cursor, save, close = get_db()
    cursor.execute("""
        insert into service (service_type, service_data, service_time, language, customer_id)
        values (?, ?, ?, ?, ?)
                   """, (service_type, service_data, service_time, langauge, customer_id))
    save()
    close()

def accept_service(empId,serviceId,customerId):
    cursor, save, close = get_db()
    cursor.execute("update service set status = 'accepted', emp_id = ? where id = ?", (empId, serviceId))
    

    mail = cursor.execute("select email from customer where id = ?", (customerId,)).fetchone()["email"]
    send_mail(mail)
    save()
    close()


def get_all_request(empId):
    cursor, _, close = get_db()
    language = cursor.execute("select language from ub_emp where id = ?", (empId,)).fetchone()
    print(language)
    tasks = []
    if language:
        tasks = cursor.execute("select * from service where language = ? and status = 'pending'", (language['language'],)).fetchall()
    close()
    print(tasks)
    return tasks