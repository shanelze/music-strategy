from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # unique = true means there would be no duplicate user
    # db.string (n) = database type, n refers to the max number of characters 
    email = db.Column(db.String (150), unique=True)
    password = db.Column(db.String (150))
    first_name = db.Column(db.String (150))
    scam = db.relationship('Scams')
    user = db.relationship('FAQ')
    chatbot = db.relationship('Chatbot')

class Scams (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.String, db.ForeignKey ('user.id'))

class FAQ (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_response = db.Column (db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.String, db.ForeignKey ('user.id'))

class Chatbot (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chatbot_response = db.Column (db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.String, db.ForeignKey ('user.id'))

class Topic (db.Model):
    title = db.Column(db.String(150), unique=True, nullable=False, primary_key=True)
    description = db.Column(db.String, nullable=False)
    thread = db.relationship('Thread')

class Thread (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    topic_title = db.Column(db.String, db.ForeignKey ('topic.title'))
    comment = db.relationship ('Comment')

class Comment (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column (db.String, nullable=False)
    thread_id = db.Column (db.Integer, db.ForeignKey('thread.id'))
    date = db.Column(db.DateTime, default=datetime.now)
    gemini_comment = db.relationship('GeminiComment')

class GeminiComment (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response = db.Column (db.String, nullable=False)
    thread_id = db.Column (db.Integer)
    date = db.Column(db.DateTime, default=datetime.now)
    comment_id = db.Column(db.Integer, db.ForeignKey ('comment.id'))