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
TRA = "transactions"
SAL = "sales"

#product id list
#product id must be unique, so everytime i add a product its id will be stored here to check whether id is duplicated or not
pid_list = []
cid_list = []

#bill dictionary
#it will store the p_id of products and their count as key value pair
bill = {}
total = 0

_user = input("username: ")
_passwd = input("password: ")

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
  
def display_customer(c_id: int):
  q = connector.where_query(mydb, CUS, ("name", ), ("c_id",), (c_id, ) )
  return q[0][0]

def get_product_name(p_id: int):
  q = connector.where_query(mydb, INV, ("name", ), ("p_id", ), (p_id, ))
  return q[0][0]

def get_product_unit_price(p_id: int):
  q = connector.where_query(mydb, INV, ("unit_price", ), ("p_id", ), (p_id, ))
  return q[0][0]

def add_sales(p_id :int, day: date, count: int):
  connector.insert_values(mydb, SAL, (p_id, day, count))

def add_transaction(c_id: int, amount: int):
  connector.insert_values(mydb, TRA, (c_id, amount))

def show_bill():
  t_price = 0
  for x in bill:
    line = str(get_product_name(x)) + ": " + str(bill[0])  + "\n"
    print(line)
    t_price += get_product_unit_price(x) * bill[0]

  print("Total: ", t_price)

def complete_transaction(c_name : str, day : date):
  #decrement items from inv
  for x in bill:
    decrement_product_in_inv(x, bill[x])
    add_sales(x, day, bill[x])

    #todo search for customer if its not in table make new customer with new id and then modify sales and transaction tables
  reset_bill()

def main():
  #todo get date
  c_name = input("Customer name> ")
  fetch_pid_list()
  fetch_cid_list()

  add_product_to_bill(0, 50)
  show_bill()

main()

      



