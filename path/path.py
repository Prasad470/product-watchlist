

from flask import *
from flask import Flask
from sqlalchemy import text
#from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
import os 
import sqlalchemy as db
from flask import Blueprint
path=Blueprint("path",__name__,static_folder="static")
app = Flask(__name__)




UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#UPLOAD_FOLDER = 'static/uploads'
#ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
#path.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Defining the Engine
#engine=db.create_engine("postgresql://postgres:admin@localhost:5432/test1", echo=True)
#engine = db.create_engine("postgresql://rtrhmetlvhpaeg:4def93b38a7244c27528694434fab9a34739ce583a772b037d4b947e538ca751@ec2-44-209-24-62.compute-1.amazonaws.com:5432/d1uo9krvi1hdrl", echo=True)
engine = db.create_engine("postgresql://usacdnlbd1hxa1aldihe:exjJHJrifsZXPKy3xmvT@blmhzjk3ytksex7ddjbe-postgresql.services.clever-cloud.com:5432/blmhzjk3ytksex7ddjbe", echo=True)

#with app.app_context():
#	db.create_all()
def getLoginDetails():
	if 'email' not in session:
		loggedIn = False
		firstName = ''
		noOfItems = 0
	else:
		loggedIn = True
		sql=text('''SELECT "userId", "firstName" FROM users where email = '{}' '''.format(session['email']) )
		results = engine.execute(sql)
		a=results.fetchall()
		userId=a[0][0]
		firstName = a[0][1]
		sql= text('''SELECT  count("productId_kart")
	FROM kart where "userId_kart" = {} '''.format(userId))
		results=engine.execute(sql)
		b = results.fetchall()
		noOfItems= b[0][0]
	return(loggedIn, firstName, noOfItems)

@path.route("/")
def root():
	loggedIn, firstName, noOfItems = getLoginDetails() 
	sql=text('''SELECT "productId", name, price, description, image, stock
	FROM public.products''')
	results = engine.execute(sql)
	itemData = results.fetchall()
	sql=text('''SELECT "categoryId", name
	FROM public.categories''')
	results = engine.execute(sql)
	categoryData = results.fetchall()
	itemData = parse(itemData)   
	return render_template('home.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryData=categoryData)




@path.route("/add")
def admin():
	sql=text('''SELECT "categoryId", name
	FROM public.categories''')
	results = engine.execute(sql)
	categoryData = results.fetchall()
	return render_template('add.html', categories=categoryData)



@path.route("/addItem", methods=["GET", "POST"])
def addItem():
	if request.method == "POST":
		name = request.form['name']
		price = request.form['price']
		description =request.form['description']
		stock = request.form['stock']
		categoryId = int(request.form['category'])

        #Uploading image procedure
		image = request.files['image']
		if image and allowed_file(image.filename):
			filename = secure_filename(image.filename)
			image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		imagename = filename

		sql=text('''INSERT INTO public.products( name, price, description, image, stock, "categoryId") VALUES ('{}', '{}', '{}', '{}', '{}',{})'''.format(name, price, description, imagename, stock, categoryId))
		results = engine.execute(sql)
		print(results)

	return redirect(url_for('path.root'))
@path.route("/remove")
def remove():
    sql=text('''SELECT "productId", name, price, description, image, stock, "categoryId" FROM public.products''')
    results = engine.execute(sql)
    data = results.fetchall()
    return render_template('remove.html', data=data)

@path.route("/removeItem")
def removeItem():
	productId = request.args.get('productId')
	try:
		sql=text('''DELETE FROM public.products WHERE "productId" = {}'''.format(productId))
		results = engine.execute(sql)
		print(results)
		msg = "Deleted successsfully"
	except:
		msg = "Error occured"

	print(msg)
	return redirect(url_for('path.root'))

@path.route("/displayCategory")
def displayCategory():
	loggedIn, firstName, noOfItems = getLoginDetails()
	categoryId = request.args.get("categoryId")
	
	sql=text('''SELECT products."productId" ,products.name, products.price, products.image, categories.name FROM products INNER JOIN categories on categories."categoryId" = products."categoryId" 
    WHERE categories."categoryId" = {}'''.format(categoryId))
	results = engine.execute(sql)
	data = results.fetchall()
	categoryName = data[0][4]
	data = parse(data)
	return render_template('displayCategory.html', data=data, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryName=categoryName)

@path.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('path.root'))
    else:
        return render_template('login.html', error='')



@path.route("/register", methods = ['GET', 'POST'])
def register():
	if request.method == 'POST':
		password = request.form['password']
		email = request.form['email']
		firstName = request.form['firstName']
		lastName = request.form['lastName']
		address1 = request.form['address1']
		address2 = request.form['address2']
		zipcode = request.form['zipcode']
		city = request.form['city']
		state = request.form['state']
		country = request.form['country']
		phone = request.form['phone']
		try:
			sql=text('''INSERT INTO public.users(
	 password, email, "firstName", "lastName", address1, address2, zipcode, city, state, country, phone)
	VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(password,email,firstName,lastName,address1,address2,zipcode,city,state,country,phone))
			results = engine.execute(sql)
			msg='Registred Successfull'	
		except:
			msg='Error Occured'
		return render_template("login.html", error=msg)

@path.route("/registerationForm")
def registrationForm():
    return render_template("register.html")

@path.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('path.root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)


@path.route("/productDescription")
def productDescription():
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = request.args.get('productId')
    sql = text('''SELECT "productId", name, price, description, image, stock
	FROM public.products WHERE "productId" = {}'''.format(productId))
    results = engine.execute(sql)
    productData=results.fetchall()[0]
    return render_template("productDescription.html", data=productData, loggedIn = loggedIn, firstName = firstName, noOfItems = noOfItems)


@path.route("/cart")
def cart():
	if 'email' not in session:
		return redirect(url_for('path.loginForm'))
	loggedIn, firstName, noOfItems = getLoginDetails()
	email = session['email']
	sql = text('''SELECT "userId" from users where email = '{}' '''.format(email))
	results = engine.execute(sql)
	userId = results.fetchall()[0][0]
	sql = text('''SELECT products."productId" ,products.name, products.price, products.image FROM products INNER JOIN kart on kart."productId_kart" = products."productId" WHERE kart."userId_kart" ={} '''.format(userId))
	results = engine.execute(sql)
	products=results.fetchall()
	print(products)
	totalPrice = 0
	for row in products:
		totalPrice += int(row[2])
	return render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)


@path.route("/addToCart")
def addToCart():
	if 'email' not in session:
		return redirect(url_for('path.loginForm'))
	else:
		productId = int(request.args.get('productId'))
		email=session['email']
		sql = text('''SELECT "userId" from users where email = '{}' '''.format(email))
		results = engine.execute(sql)
		userId = results.fetchall()[0][0]
	try:
		sql=text(''' INSERT INTO public.kart("userId_kart", "productId_kart") VALUES ( '{}', '{}')'''.format(userId, productId))
		results= engine.execute(sql)
		msg = "Added successfully"
	except:
		
		msg = "Error occured"
	
	return redirect(url_for('path.root'))



@path.route("/removeFromCart")
def removeFromCart():
	if 'email' not in session:
		return redirect(url_for('path.loginForm'))
	email=session['email']
	productId = int(request.args.get('productId'))
	sql = text('''SELECT "userId" from users where email = '{}' '''.format(email))
	results = engine.execute(sql)
	userId = results.fetchall()[0][0]
	try:
		sql = text('''DELETE FROM kart WHERE "userId_kart"={} AND "productId_kart"= {}'''.format(userId,productId))
		print(sql)
		results = engine.execute(sql)
		msg = "removed successfully"
		
	except:
		msg="error"
	print(msg)
	return redirect(url_for('path.root'))

@path.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('path.root'))

def is_valid(email, password):
    sql=text( '''select email,password from users ''')
    data = engine.execute(sql)
    for row in data:
        if row[0] == email and row[1] == password:
            return True
    return False



def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

	

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans



#metadata_obj.create_all(engine)

#if __name__ == '__main__':
 #   app.run(debug=True)

	
