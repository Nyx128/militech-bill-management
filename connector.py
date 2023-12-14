import mysql.connector


##module made for convinient usage of common sql operations

def connect(u, p, d_name):
  return mysql.connector.connect(
    host="localhost",
    user=u,
    password=p,
    database=d_name
)

def insert_values(db, table_name, data):
  #generate insert list to take a tuple with arbitrary length
  insert_list = ""
  for x in range(len(data)):
    if(x!=len(data)-1):
      insert_list += "%s,"
    else:
      insert_list += "%s"

  cmd = "INSERT INTO " + table_name + " values(" + insert_list + ");"
  cur = db.cursor()
  cur.execute(cmd, data)
  db.commit()

def delete_row(db, table_name, check, value):
  con_list = ""
  for x in range(len(check)):
    if x != len(check)-1:
      con_list += check[x] + "=%s and "
    else:
      con_list += check[x] + "=%s" 
  data = value
  cmd = "DELETE FROM " + table_name + " WHERE " + con_list + ";"
  cur = db.cursor()
  cur.execute(cmd, data)
  db.commit()

def where_query(db, table_name, selection, check, value):
  #create a check list from the check tuple and compare its corresponding value from value
  con_list = ""
  for x in range(len(check)):
    if x != len(check)-1:
      con_list += check[x] + "=%s and "
    else:
      con_list += check[x] + "=%s"

  selection_list = ""
  for x in range(len(selection)):
    if x != len(selection)-1:
      selection_list += selection[x] + ", "
    else:
      selection_list += selection[x]
  data = value
  cmd = "SELECT " + selection_list + " FROM " + table_name + " WHERE " + con_list + ";"
  cur = db.cursor()
  cur.execute(cmd, data)
  return cur.fetchall()
