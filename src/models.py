from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from base64 import b64encode

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password=db.Column(db.String(120),unique=False, nullable=False)
    salt=db.Column(db.String(120), nullable=False)
    
    bills=db.relationship("Bill",backref="user")

    @classmethod
    def create(cls,**kwargs):
        new_user=cls(kwargs)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    def __init__(self, body):
        self.email=body ['email']
        self.username=body['username']
        self.salt=b64encode(os.urandom(4)).decode("utf-8")
        self.hashed_password=self.set_password(body['pass'])
        
    def set_password(self, password):
        return generate_password_hash(
            f"{password}{self.salt}"
        )

    def check_password(self, password):
        print(f"este es el password:{password}")
        return check_password_hash(
            self.hashed_password,
            f"{password}{self.salt}"
        )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
        }
        
class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_bill = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    value = db.Column(db.Numeric(9))
    type = db.Column(db.Integer)
    observation = db.Column(db.String(120))
    

    def __init__(self,body):
        self.date_bill=body['date_bill']
        self.user_id=body['user_id']
        self.value=body['value']
        self.type=body['type']
        self.observation=body['observation']
       

    @classmethod
    def create_bill(cls,**kwargs):
        new_bill=cls(kwargs)
        db.session.add(new_bill)
        db.session.commit()
        return new_bill
    
    def serialize(self):
        return {
            "id": self.id,
            "date_bill": self.date_bill,
            "user_id": self.user_id,
            "value": self.value,
            "type": self.type,
            "observation": self.observation,
        }