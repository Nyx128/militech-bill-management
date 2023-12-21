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
customer_list = []

#bill dictionary
#it will store the p_id of products and their count as key value pair
bill = {}
total = 0

_user = input("username: ")
_passwd = input("password: ")

mydb = connector.connect(_user, _passwd, "militech")

def fetch_pid_list():
  pid_list.clear()
  cur = mydb.cursor()
  query = "SELECT p_id from " + INV + ";"
  cur.execute(query)
  d = cur.fetchall()
  for x in d:
    pid_list.append(x[0])
  cur.close()

def fetch_cid_list():
  cid_list.clear()
  cur = mydb.cursor()
  query = "SELECT c_id from " + CUS + ";"
  cur.execute(query)
  d = cur.fetchall()
  for x in d:
    cid_list.append(x[0])
  cur.close()

def fetch_customers():
  customer_list.clear()
  cur = mydb.cursor()
  query = "SELECT name from " + CUS + ";"
  cur.execute(query)
  d = cur.fetchall()
  for x in d:
    customer_list.append(x[0])
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
  name = q[0][0]
  q = connector.where_query(mydb, TRA, ("amount", ), ("c_id", ), (c_id, ))
  amount = 0
  for x in q:
    amount += x[0]
  print("name: ", name)
  print("Total spent: ", amount)

def get_cid(c_name: str):
  q = connector.where_query(mydb, CUS, ("c_id",), ("name", ), (c_name, ))
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
  amount = 0
  #decrement items from inv
  #add stats to sales
  #add the transaction to the transactions table
  for x in bill:
    decrement_product_in_inv(x, bill[x])
    add_sales(x, day, bill[x])
    amount = amount + (get_product_unit_price(x) * bill[x])

  if c_name not in customer_list:
    c = max(cid_list) +1
    add_customer(c, c_name)
    fetch_customers()
    fetch_cid_list()
    add_transaction(c, amount)
  else:
    c = get_cid(c_name)
    add_transaction(c, amount)
    
  reset_bill()

def ask_filtered_input(prompt: str, filter, err: str):
  i = input(prompt)
  if i not in filter:
    print(err)
    ask_filtered_input(prompt, filter, err)
  else:
    return i
  
def wait_for_next():
  input("Press any key to continue: ")

def clamped_input(l: int, h:int, desc: str):
  #input will be accepted only if its between l and h (inclusive)
  i = int(input(desc))
  if i not in range(l, h+1):
    clamped_input(l, h, desc)
  else:
    return i

def ask_date():
  d = clamped_input(1, 31, "day(1-31)>")
  m = clamped_input(1, 12, "month(1-12)>")
  y = clamped_input(1, 9999,"year(1-9999)>")
  return date(y, m, d)


def sample_input():
  funcs = ["api", "rpi", "ipi", "dpi", "apb", "rpb", "ipb","dpb","rb", "dc", "sb", "ct", "quit"]
  func_list = """functions: 
          api(add product to inventory)
          rpi(remove product from inventory)
          ipi(increment product in inventory)
          dpi(decrement product in inventory)
          apb(add product to bill)
          rpb(remove product from bill)
          ipb(increment product in bill)
          dpb(decrement product in bill)
          rb(reset bill)
          dc(display customer)
          sb(show bill)
          ct(complete transaction)
          quit"""
  print(func_list)
  
  cmd = ask_filtered_input("Input function>", funcs, "Please input one function from the list as it is")
  print("\n\n")
  if cmd == "quit":
    exit()
  elif cmd == "api":
    id = max(pid_list) + 1
    n = input("product name> ")
    p = int(input("unit price> "))
    c = int(input("count> "))
    print("\n")
    add_product_to_inv(id, n, p, c)
    fetch_pid_list()
    wait_for_next()
    sample_input()
  elif cmd == "rpi":
    id = int(input("product id> "))
    print("\n")
    rem_product_from_inv(id)
    wait_for_next()
    sample_input()
  elif cmd == "ipi":
    id = int(input("product id> "))
    c = int(input("Increment count> "))
    print("\n")
    increment_product_in_inv(id, c)
    wait_for_next()
    sample_input()
  elif cmd == "dpi":
    id = int(input("product id> "))
    c = int(input("Decrement count> "))
    print("\n")
    decrement_product_in_inv(id, c)
    wait_for_next()
    sample_input()
  elif cmd == "apb":
    id = int(input("product id> "))
    c = int(input("count: "))
    add_product_to_bill(id, c)
    print("\n")
    wait_for_next()
    sample_input()
  elif cmd == "rpb":
    id = int(input("product id> "))
    rem_product_from_bill(id)
    print("\n")
    wait_for_next()
    sample_input()
  elif cmd == "ipb":
    id = int(input("product id> "))
    c = int(input("Increment count> "))
    increment_product_in_bill(id, c)
    print("\n")
    wait_for_next()
    sample_input()
  elif cmd == "dpb":
    id = int(input("product id> "))
    c = int(input("Decrement count> "))
    decrement_product_in_bill(id, c)
    print("\n")
    wait_for_next()
    sample_input()
  elif cmd == "dc":
    id = int(input("customer id> "))
    display_customer(id)
    print("\n")
    wait_for_next()
    sample_input()
  elif cmd == "sb":
    show_bill()
    wait_for_next()
    sample_input()
  elif cmd == "ct":
    customer_name = input("Customer name> ")
    day = ask_date()
    complete_transaction(customer_name, day)

def main():

  print("*****************MILITECH BILLING SYSTEM*****************\n")
  
  #todo get date
  fetch_pid_list()
  fetch_cid_list()
  fetch_customers()

  sample_input()

main()

      



