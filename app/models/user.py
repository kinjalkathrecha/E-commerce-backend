from sqlalchemy import Column,Integer,String
from app.db.database import base

class User(base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True,index=True)
    password=Column(String)