from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import pbkdf2_sha256 as pbsha
from datetime import datetime, timedelta
import os

Base=declarative_base()

class Admin_model(Base):
    __tablename__="admin"

    user_id=Column(Integer, primary_key=True)
    username=Column(String)
    password_hash=Column(String)
    token=Column(String)
    token_expiry=Column(DateTime)

    def set_password(self, password):
        self.password_hash=pbsha.hash(password)

    def check_password(self, password):
        return pbsha.verify(password, self.password_hash)

    def get_token(self):
        self.token=os.urandom(3).hex()
        self.token_expiry=datetime.utcnow()+timedelta(seconds=360)
        return self.token

    def validate_token(self):
        return (datetime.utcnow()+timedelta(seconds=60))<self.token_expiry

    def invalidate_token(self):
        self.token_expiry=datetime.utcnow()-timedelta(seconds=5)
        return

class Emp_model(Base):
    __tablename__="employee"

    id=Column(Integer, primary_key=True)
    name=Column(String(64))
    age=Column(Integer)
    ed=Column(String(64))
    role=Column(String(64))
