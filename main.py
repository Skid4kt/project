from flask import Flask,render_template,redirect,url_for,request,flash,session
from dbservice import get_data,sales_product,profit,sales_daily,profit_daily,resales,check_email,check_email_password,insert_user,insert_sale, insert_data


#create the flask instance
app = Flask(__name__)
app.secret_key="armel"
#first route 
@app.route('/')
def home():
    return render_template('home.html')



@app.route("/products")
def products():
    prods=get_data("products")
    return render_template("products.html",product=prods)
@app.route('/add_products',methods=['POST', 'GET'])
def add_products():
    if request.method == "POST":
        pname = request.form['product_name']
        bprice = request.form['buying_price']
        sprice = request.form['selling_price']
        squantity = request.form['stock_quantity']
        # insert into db
        new_prod = (pname, bprice, sprice, squantity)
        insert_data(new_prod)
        flash('product added successfuly')


    return redirect(url_for('products'))


@app.route("/sales")
def sales():
    sal=get_data("sales")
    prod=get_data("products")
    return render_template("sales.html",sales=sal,products=prod)
@app.route('/make_sale',methods=['GET', 'POST'])
def make_sale():
    if request.method == 'POST':
        product_name = request.form['product_name']
        quantity = request.form['quantity']
        new_sale=(product_name, quantity)
        insert_sale(new_sale)
        flash('Sale made')

    return redirect(url_for('sales'))

@app.route("/dashboard")
def dashboard():
    sale_p=sales_product()
    p_name=[]
    p_sales=[]

    for i in sale_p:
        p_name.append(i[0])
        p_sales.append(float(i[1]))
    
    pr=profit()
    rr=[]
    
    for i in pr:
        rr.append(float(i[1]))


    s_d=sales_daily()
    date=[]
    sales_d=[]
    for i in s_d:
        date.append(str(i[0]))
        sales_d.append(float(i[1]))

    p_d=profit_daily()
    date=[]
    profits_d=[]
  
    for i in p_d:
        date.append(str(i[0]))
        profits_d.append(float(i[1]))
    print("kiswahili",date)
    print("kikombe",profits_d)
    # r_s=resales()
    # date=[]
    # r_sales=[]
    # for i in r_s:
    #       date.append(str(i[0]))
    #       r_sales.append(float(i[1]))

    r_s=resales()
    return render_template("dashboard.html",p_name=p_name,\
                           
                           p_sales=p_sales,rr=rr,date=date,sales_d=sales_d,profits_d=profits_d,r_s=r_s)


@app.route('/login',methods=['POST', "GET"])
def login():
   
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        c_mail= check_email(email)
        print (c_mail)
        if len(c_mail) == 1:
            session['email']=email
            check_em_ps = check_email_password(email,password)
            if len(check_em_ps) == 1:
                flash('You were successfully logged in')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials')
        else:
            flash ('Email does not exists')
            redirect(url_for('register'))

    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop("email",None)
    return redirect(url_for("home"))



# create dashboard
@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        uname = request.form['full_name']
        mail=  request.form['email']
        passw = request.form['password']

        
        new_user =(uname,mail,passw)
        c_email=check_email(mail)
        print (c_email)
        if len(c_email) == 0:
            insert_user(new_user)
            flash ("registered successfuly")
            return redirect(url_for('login'))
        else:
            flash ('Email already exists')

    return render_template('register.html')

    
app.run(debug=True)