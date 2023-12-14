#this script is to be run once to setup the appropriate database and tables
#note the following database name should not exist beforehand - school_db

import connector

_user = input("username: ")
_passwd = input("password: ")

mydb = connector.connect(_user, _passwd)

cur = mydb.cursor()

cur.execute("CREATE TABLE students(name varchar(64), class int, roll int, address varchar(128), ph int);")
cur.execute("CREATE TABLE teachers(name varchar(64), post varchar(64), salary int, address varchar(128), ph int, acc_no int);")
cur.execute("CREATE TABLE fees(name varchar(64), class int, roll int, month int);")
cur.execute("CREATE TABLE salary(name varchar(64), month int, paid int, acc_no int);")
cur.execute("CREATE TABLE s_attendance(day date, class int, absent int);")
cur.execute("CREATE TABLE t_attendance(day date, absent int);")
mydb.commit()

print("SCHOOL MANAGEMENT SYSTEM initialization complete")