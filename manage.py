import click
from flask.cli import with_appcontext
from flask import *
import sqlalchemy as db
from sqlalchemy import text
import click



#engine =db.create_engine("postgresql://postgres:admin@localhost:5432/mydb", echo=True)
engine = db.create_engine("postgresql://whrqxdrsctgpje:6fe1cfdd46b896ad284762304ba8486d2b430726fd739f679c6c3e838c079dcc@ec2-44-199-9-102.compute-1.amazonaws.com:5432/d5bplkt2v50bbi", echo=True)

# Create the Metadata Object
metadata_obj = db.MetaData()

from app import db
from .models import User, Question

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    metadata_obj.create_all(engine)