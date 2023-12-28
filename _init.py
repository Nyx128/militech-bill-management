#this script is to be run once to setup the appropriate database and tables
#note the following database name should not exist beforehand - school_db

import mysql.connector

_user = input("username: ")
_passwd = input("password: ")

mydb = mysql.connector.connect(
    host="localhost",
    user=_user,
    password=_passwd)

cur = mydb.cursor()

cur.execute("CREATE database militech")
cur.execute("use militech")
cur.execute("CREATE TABLE inventory(p_id int primary key, name varchar(512), unit_price int, count int);")
products = [("Militech M-179 Achilles", 40000), ("Militech M-10AF Lexington", 34000), ("Militech M221 Saratoga",25000) , ("Militech Crusher", 12000), ("Militech M251s Ajax",45000),
            ("Militech Mk. 31 HMG", 31000),("Militech Basilisk", 9000),("Militech Behemoth", 56000), ("Militech Manticore", 23000), ("Militech Berserk Mk.5", 59000)]
for x in range(10):
  cmd = "INSERT INTO inventory values(" + str(x) + ", \"" + products[x][0] + "\", " + str(products[x][1]) + ", " + "999);"
  cur.execute(cmd)

cur.execute("CREATE TABLE customers(c_id int primary key, name varchar(512))")
cur.execute("CREATE TABLE transactions(c_id int, amount int)")
cur.execute("CREATE TABLE sales(p_id int, day date, count int)")
mydb.commit()

print("SCHOOL MANAGEMENT SYSTEM initialization complete")