from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tablas2.db'

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    comments = db.relationship('Comment')

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    idUser = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/set')
def set():
    with app.app_context():
        s = db.session()
        user = User(name='Fulano')
        s.add(Comment(text='comentario 1', idUser=1))
        s.add(Comment(text='comentario 2', idUser=1))
        s.add(Comment(text='comentario 3', idUser=1))
        s.add(user)
        s.commit()
    return render_template('home.html')

@app.route('/get')
def get():
    with app.app_context():
        s = db.session()
        usuario = s.query(User).filter(User.name == 'Fulano').one()
        print ("employees: {}".format(usuario.comments))
        print ("empleat zero: {}".format(usuario.comments[0].text))
        for t in usuario.comments:
            print ("{}".format(t.text))
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
