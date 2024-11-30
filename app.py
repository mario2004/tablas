from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tablas.db'

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    comments = db.relationship('Comment')
    def to_dict(self):
        obj={}
        array=[]
        for item in self.comments:
            obj['id']=item.id
            obj['text']=item.text
            array.append(obj) # TODO flipante, aquí cambia el valor de array que supuestamente es una variable local.
        return{
            'id' : self.id,
            'name' : self.name,
            'comments': array
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    idUser = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    def to_dict(self):
        return{
            'id' : self.id,
            'text' : self.text,
        }

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/set')
def set():
    with app.app_context():
        s = db.session()
        user = User(name='Mengano')
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
        obj = usuario.to_dict()
    return render_template('home.html', usuario=obj)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
