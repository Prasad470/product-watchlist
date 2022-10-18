import click
from flask.cli import with_appcontext
from flask import *
import sqlalchemy as db
from sqlalchemy import text
import click



#engine =db.create_engine("postgresql://postgres:admin@localhost:5432/mydb", echo=True)
engine = db.create_engine("postgresql://rtrhmetlvhpaeg:4def93b38a7244c27528694434fab9a34739ce583a772b037d4b947e538ca751@ec2-44-209-24-62.compute-1.amazonaws.com:5432/d1uo9krvi1hdrl", echo=True)

# Create the Metadata Object
metadata_obj = db.MetaData()

from app import db
from .models import User, Question

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    metadata_obj.create_all(engine)