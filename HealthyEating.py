import mysql.connector
import requests
import json

mydb = mysql.connector.connect (
    host = "localhost",
    user = "root",
    password = "pass1234",
    database = "culinarydatabase"
)





def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sorts_key=True, indent = 4)
    print(text)

#jprint(response.json())

mycursor = mydb.cursor()

class Fridge:
    def __init__(self):
        self.name = "Fridge"
        self.items = {}
    def set_amount(self, ingredient_name):
        print(f"{ingredient_name}: {self.items[ingredient_name]}")
        self.items[ingredient_name] = int(input("Enter new amount: "))
    def consume(self, howmany):
        print("{0} {1}s consumed!".format(howmany, self.name))

# SQ
def set_ingredient(ingredient_name):
    parameters = {
    "app_id": "29a8e8e7",
    "app_key": "a65e53083e63c84638b5535733a81d07",
    "ingr": ingredient_name
    }
    response = requests.get("https://api.edamam.com/api/food-database/v2/parser", params=parameters).text
    response_info = json.loads(response)
    #print(response_info["hints"][1]["food"])
    
    complete = False
    i = 0
    while not complete:
        print(i)
        name = response_info["hints"][i]["food"]["label"]
        brand = response_info["hints"][i]["food"]["brand"]
        calories = response_info["hints"][i]["food"]["nutrients"]["ENERC_KCAL"]
        protein = response_info["hints"][i]["food"]["nutrients"]["PROCNT"]
        fat = response_info["hints"][i]["food"]["nutrients"]["FAT"]
        carbohydrates = response_info["hints"][i]["food"]["nutrients"]["CHOCDF"]
        fiber = response_info["hints"][i]["food"]["nutrients"]["FIBTG"]

        acceptance = input("Name: {name}, Brand: {}, " + " ")
        if acceptance == "y":
            # code
            print(f"The ingredient {ingredient_name} has been added.")
            complete = True
        elif acceptance == "n":
            i += 1
        elif acceptance == "q":
            break


set_ingredient("turkey slice")


# SQL Table Functions
def create_table(table_name, conds):
    mycursor.execute(f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, {conds})")
def alter_table(table_name, cond):
    mycursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {cond}")
def show_tables():
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        print(x)
def delete_record(table_name, cond, operation, term):
    sql = f"DELETE FROM {table_name} WHERE {cond} {operation} %s"
    val = (term, )
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")
def delete_table(table_name):
    mycursor.execute(f"DROP TABLE IF EXISTS {table_name}")

# SQL Select Functions
def select_all(table_name):
    mycursor.execute(f"SELECT * FROM {table_name}")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
def select_where(table_name, cond, operation, term):
    sql = f"SELECT * FROM {table_name} WHERE {cond} {operation} %s"
    val = (term, )
    mycursor.execucte(sql,val)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
def select_order(table_name, term, descending = False):
    desc = 'DESC' if descending else ''
    sql = f"SELECT * FROM {table_name} ORDER BY {term} {desc}"
    mycursor.execucte(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
def select_limit(table_name, limit):
    mycursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
def select_limit_offset(table_name, limit, offset):
    mycursor.execute(f"SELECT * FROM {table_name} LIMIT {limit} OFFSET {offset}")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

# SQL Insert Functions
def insert_customer(table_name, name, address):
    sql = f"INSERT INTO {table_name} (name, address) VALUES (%s, %s)"
    val = (name, address)
    mycursor.execute(sql,val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
def insert_customers(table_name, input_list):
    sql = f"INSERT INTO {table_name} (name, address) VALUES (%s, %s)"
    val = input_list
    mycursor.executemany(sql,val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
def update_table(table_name, cond, set_op, set_term, where_op, where_term):
    sql = f"UPDATE {table_name} SET {cond} {set_op} %s WHERE {cond} {where_op} %s"
    val = (set_term, where_term)
    mycursor.execute(sql,val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")

# SQL Join Functions
def inner_join(text):
    sqlex = "SELECT \
        users.name AS user, \
        products.name AS favorite \
        FROM users \
        INNER JOIN products ON user.fav = products.id"  #INNER JOIN interchangeable with JOIN
    sql = text
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
def left_join(text):
    sqlex = "SELECT \
        users.name AS user, \
        products.name AS favorite \
        FROM users \
        LEFT JOIN products ON user.fav = products.id"
    sql = text
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
def right_join():
    sql = "SELECT \
        users.name AS user, \
        products.name AS favorite \
        FROM users \
        RIGHT JOIN products ON user.fav = products.id"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


#create_table("food", "name VARCHAR(255) NOT NULL UNIQUE, calories DOUBLE, recipes TEXT")
#show_tables()
