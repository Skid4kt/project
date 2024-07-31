import psycopg2


conn=psycopg2.connect(
    dbname="myduka",
    user="postgres",
    host="localhost",
    password="armelNN23",
    port=5432


)

cur=conn.cursor()
#fetch products
#def get_products():
 #   query="select * from products"
  #  cur.execute(query)
   # products=cur.fetchall()
    #print(products)

#get_products()

#fetch sales
#def get_sales():
 #   query="select * from sales"
  #  cur.execute(query)
   # sales=cur.fetchall()
    #print(sales)

#get_sales()    

#def get_data(a,b):
 #   query="select * from a and b"
  #  cur.execute(query)
   # data=cur.fetchall()
    #print(data)

def get_data(table):
    query=f"select * from {table}"
    cur.execute(query)
    data=cur.fetchall()
    return data

# get_data("sales")

# #insert
# def insert_products():
#     query = "insert into products(id,name,buying_price,selling_price,stock_quantity)values(100,'ginger',100,200,10)"
#     cur.execute(query)
#     conn.commit()



# make sale
def insert_sale(values):
    query ="INSERT INTO sales (productid, quantity, created_at) VALUES (%s, %s, now());"
    cur.execute(query,values)
    conn.commit()

def insert_data(values):
    query = "INSERT INTO products(name, buying_price, selling_price, stock_quantity) values(%s,%s,%s,%s);"
    cur.execute(query, values)
    conn.commit()



# 1
# def calc_sales_day():
#     query = "SELECT DATE(s.created_at) AS sale_date/
#     Sum(s.quantity * p.selling_price) AS total_sales"



def sales_product():
    query = "SELECT name,SUM(p.selling_price * s.quantity)\
        As totsales FROM sales as s JOIN products as p ON s.id = p.id\
            GROUP BY p.name;"
    cur.execute(query)
    data= cur.fetchall()
    
    return data



def profit():
    query = "SELECT p.name, SUM((p.selling_price - p.buying_price)\
        * s.quantity) AS profit FROM sales as s JOIN products as p ON s.productid = p.id GROUP BY p.name"
    cur.execute(query)
    data= cur.fetchall()
    return data

def sales_daily():
    query = "SELECT DATE(s.created_at) AS sales_day,SUM(p.selling_price * s.quantity) \
        AS sales FROM sales s JOIN products p ON s.productid = p.id GROUP BY sales_day ORDER BY sales_day"
    cur.execute(query)
    data = cur.fetchall()
    return data

def profit_daily():
    query = "SELECT DATE(sales.created_at)as profit_day,\
        sum((products.selling_price - products.buying_price)*sales.quantity)\
        AS profit from sales JOIN products on sales.productid = products.id \
        GROUP BY profit_day order by profit_day;"
    cur.execute(query)
    data = cur.fetchall()
    return data

def resales():
    query = "select * from sales ORDER BY sales.created_at limit 10;"
    cur.execute(query)
    r_sales=cur.fetchall()
    return r_sales

def insert_user(values):
    query= "insert into users(full_name,email,password)values(%s,%s,%s)"
    cur.execute(query,values)
    conn.commit()

def check_email(email):
    query = "SELECT * FROM users WHERE email = %s"
    cur.execute(query,(email,))
    data = cur.fetchall()
    return data

def check_email_password(email,password):
    query='SELECT * FROM users WHERE email=%s and password=%s'
    cur.execute(query,(email,password))
    data = cur.fetchall()
    return data

