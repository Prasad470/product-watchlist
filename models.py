from flask import *
import sqlalchemy as db
from sqlalchemy import text
import click



#engine =db.create_engine("postgresql://postgres:admin@localhost:5432/mydb", echo=True)
engine = db.create_engine("postgresql://rtrhmetlvhpaeg:4def93b38a7244c27528694434fab9a34739ce583a772b037d4b947e538ca751@ec2-44-209-24-62.compute-1.amazonaws.com:5432/d1uo9krvi1hdrl", echo=True)

# Create the Metadata Object
metadata_obj = db.MetaData()

kart = db.Table(
	'kart',										
	metadata_obj,
								
	db.Column('userId_kart',db.Integer,db.ForeignKey("users.userId")),
	db.Column('productId_kart',db.Integer,db.ForeignKey("products.productId")),				
)



customer= db.Table(
	'customer',
	metadata_obj,
    db.Column('id',db.Integer, primary_key=True, nullable=False),
    db.Column('name',db.String(45), nullable=False),
    db.Column('email',db.String(45), nullable=False),
    db.Column('phone',db.String(45), nullable=False),
    db.Column('currentBalance',db.String(20), nullable=False),
    db.Column('accountNo',db.Integer, nullable=False),
    db.Column('time',db.String(45), nullable=False),
)


Members = db.Table (
	'members',
	metadata_obj,
	db.Column('id',db.Integer, primary_key=True),
    db.Column('firstname',db.String(30)),
    db.Column('lastname',db.String(30)),
    db.Column('phoneno',db.Integer),
    db.Column('email',db.String(30)),
    db.Column('joindate',db.String(11)),
    db.Column('startdate',db.String(11)),
    db.Column('enddate',db.String(11)),
    db.Column('address',db.String(100)),
    db.Column('status',db.String(10)),
    db.Column('training',db.String(10)),
    db.Column('amount',db.Integer),
)



Users= db.Table(
	'Users',
	metadata_obj,
	db.Column('name',db.String(50), nullable=False, primary_key=True),
	db.Column('username',db.String(20), unique=True, nullable=False),
	db.Column('password',db.String(20), unique=True, nullable=False),

 )



users = db.Table(
	'users',
	metadata_obj,
	db.Column('userId' ,db.Integer,primary_key=True),
	db.Column('password', db.String()),
	db.Column('email',db.String()),
	db.Column( 'firstName',db.String()),
	db.Column('lastName',db.String()),
	db.Column('address1',db.String()),
	db.Column('address2',db.String()),
	db.Column('zipcode',db.String()),
	db.Column('city',db.String()),
	db.Column('state',db.String()),
	db.Column('country',db.String()),
	db.Column('phone',db.String()),
)
products = db.Table(
	'products',
	metadata_obj,
	db.Column('productId', db.Integer,primary_key=True,autoincrement=True),
	db.Column('name', db.String()),
	db.Column('price', db.String()),
	db.Column('description', db.String()),
	db.Column('image', db.String()),
	db.Column('stock',db.String()),
	db.Column('categoryId',db.Integer, db.ForeignKey("categories.categoryId")),

)

categories = db.Table(
	'categories',
	metadata_obj,
	db.Column('categoryId',db.Integer,primary_key=True),
	db.Column('name',db.String(100)),
)

Order = db.Table(
	'Order',
	metadata_obj,
	
	db.Column('userId',db.Integer,db.ForeignKey("users.userId")),
	db.Column('productId',db.Integer,db.ForeignKey("products.productId")),
)


#with app.app_context():
#	db.create_all()




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




metadata_obj.create_all(engine)
print("success")