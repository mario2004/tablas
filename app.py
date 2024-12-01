from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tablas.db'

db = SQLAlchemy(app)

# Inicio NOTA. Este fragmento estaba en el fichero models.py y se ponía aquí un import models.py. No se sabe por qué así no funciona y no reconoce User.
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

class Request(db.Model):
    idRequest = db.Column(db.Integer, primary_key=True)
    idAppointment = db.Column(db.Integer, db.ForeignKey('appointment.idAppointment'), nullable=False)
    requestText = db.Column(db.Text, unique=True, nullable=True)
    appointment = db.relationship('Appointment', backref=db.backref('requests', lazy=True))
    def to_dict(self):
        return {
            'idRequest': self.idRequest,
            'idAppointment': self.idAppointment,
            'requestText': self.requestText,
            'appointment': self.appointment.to_dict(),
        }

class Appointment(db.Model):
    idAppointment = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user = db.relationship('User', backref=db.backref('appointments', lazy=True))
    def to_dict(self):
        return {
            'idAppointment': self.idAppointment,
            'idUser': self.idUser,
            'amount': self.amount,
            'user': self.user.to_dict(),
        }

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/set')
def set():
    with app.app_context():
        s = db.session()
        appointment = Appointment(amount=255, idUser=1)
        user = User(username='Mengano', email='email@yopmail.com')
        s.add(Request(requestText='comentario 1', idAppointment=1))
        s.add(Request(requestText='comentario 2', idAppointment=1))
        s.add(Request(requestText='comentario 3', idAppointment=1))
        s.add(user)
        s.add(appointment)
        s.commit()
    return render_template('home.html')

@app.route('/get')
def get():
    s = db.session()
    requests = s.query(Request).filter_by(idAppointment=1).all()
    return render_template('home.html', requests=requests)

@app.route('/get2')
def get2():
    s = db.session()
    requests = s.query(Request).filter_by(idAppointment=1).all()
    objetos=[request.to_dict() for request in requests]
    return render_template('home.html', requests=objetos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
