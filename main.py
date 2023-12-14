import connector
from datetime import date

#MILITECH BILL MANAGEMENT SYSTEM

#functions
#api(add product to inv)
#rpi(remove product from inv)
#ipi(increment product count in inv)
#dpi(decrement product from inv)
#apb(add product to bill)
#rpb(remove product from bill)
#ipb(increment product count in bill)
#dpb(decrement product count in bill)
#rb(reset bill)
#dc(display customer)
#sps(show product sales)
#spr(show product revenue)
#scs(show customer stats)
#sb(show bill)
#ct(complete transaction)

#inventory table
#->p_id
#->name
#->unit_price
#->count

#table definitions
INV = "inventory"
CUS = "customers"

#product id list
#product id must be unique, so everytime i add a product its id will be stored here to check whether id is duplicated or not
pid_list = []
cid_list = []

#bill dictionary
#it will store the p_id of products and their count as key value pair
bill = {}

#_user = input("username: ")
#_passwd = input("password: ")

_user = "root"
_passwd = "Ghostryder@812"

mydb = connector.connect(_user, _passwd, "militech")

def fetch_pid_list():
  cur = mydb.cursor()
  query = "SELECT p_id from " + INV + ";"
  cur.execute(query)
  d = cur.fetchall()
  for x in d:
    pid_list.append(x[0])
  cur.close()

def fetch_cid_list():
  cur = mydb.cursor()
  query = "SELECT c_id from " + CUS + ";"
  cur.execute(query)
  d = cur.fetchall()
  for x in d:
    cid_list.append(x[0])
  cur.close()

#inventory management
def add_product_to_inv(p_id :int, name :str, unit_price :int, count :int):
  if p_id not in pid_list:
    connector.insert_values(mydb, INV, (p_id, name, unit_price, count))
    pid_list.append(p_id)
  else:
    return -1
  
def rem_product_from_inv(p_id : int):
  if p_id in pid_list:
    connector.delete_row(mydb, INV, ("p_id",), (p_id,))
    pid_list.remove(p_id)
  else:
    return -1
  
def increment_product_in_inv(p_id: int, count : int):
  if p_id in pid_list:
    query = "UPDATE inventory SET count = count + %s WHERE p_id = %s ;"
    cur = mydb.cursor()
    cur.execute(query, (count, p_id))
    mydb.commit()
  else:
    return -1
  
def decrement_product_in_inv(p_id: int, count : int):
  if p_id in pid_list:
    query = "UPDATE inventory SET count = count - %s WHERE p_id = %s ;"
    cur = mydb.cursor()
    cur.execute(query, (count, p_id))
    mydb.commit()
  else:
    return -1
  
def add_product_to_bill(p_id: int, count : int):
  if p_id not in bill:
    bill[p_id]=count
  else:
    return -1
  
def rem_product_from_bill(p_id: int):
  if p_id in bill:
    del bill[p_id]
  else:
    return -1
  
def increment_product_in_bill(p_id: int, count: int):
  if p_id in bill:
    bill[p_id]=bill[p_id]-count
  else:
    return -1
  
def decrement_product_in_bill(p_id: int, count: int):
  if p_id in bill:
    bill[p_id]=bill[p_id]-count
  else:
    return -1
  
def reset_bill():
  bill.clear()

def add_customer(c_id: int, name: str):
  if c_id not in cid_list:
    connector.insert_values(mydb, CUS, (c_id, name))
    cid_list.append(c_id)
  else: return -1

def rem_customer(c_id: int):
  if c_id in cid_list:
    connector.delete_row(mydb, CUS, ("c_id",), (c_id,))
    cid_list.remove(c_id)
  else:
    return -1
  
def display_customer(cid: int):
  q = connector.where_query(mydb, CUS, ("name", ), ("c_id",), (cid, ) )
  return q[0][0]

def show_bill():
  print(bill)

def main():
  c_name = input("Customer name> ")
  fetch_pid_list()
  fetch_cid_list()

main()

      



