from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tablas.db'

db = SQLAlchemy(app)

# Inicio NOTA. Este fragmento estaba en el fichero models.py y se ponía aquí un import models.py. No se sabe por qué así no funciona y no reconoce User.
from datetime import datetime

class User(db.Model):
    __tablename__="users"
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
    idUser = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    requestText = db.Column(db.Text, nullable=True)
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
    idUser = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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

@app.route('/cita', methods=['GET', 'POST'])
def cita():
    amount = request.form['amount']
    idUser = request.form['idUser']
    with app.app_context():
        s = db.session()
        appointment = Appointment(idUser=idUser, amount=amount)
        s.add(appointment)
        s.commit()
    return render_template('home.html')

@app.route('/requestCita', methods=['GET', 'POST'])
def requestCita():
    texto = request.form['texto']
    idUser = request.form['idUser']
    idCita = request.form['idCita']
    with app.app_context():
        s = db.session()
        s.add(Request(requestText=texto, idAppointment=idCita, idUser=idUser))
        s.commit()
    return render_template('home.html')

@app.route('/get')
def get():
    s = db.session()
    requests = s.query(Request).filter_by(idAppointment=1).all()
    return render_template('home.html', requests=requests)

@app.route('/mostrarCitas', methods=['GET', 'POST'])
def mostrarCitas():
    id = request.form['idUser']
    s = db.session()
    citasDB = s.query(Appointment).filter_by(idUser=id).all()
    citasJSON=[cita.to_dict() for cita in citasDB]
    for cita in citasJSON:
        requestsDB = s.query(Request).filter_by(idAppointment=cita['idAppointment']).all()
        requestsJSON=[request.to_dict() for request in requestsDB]
        cita['requests']=requestsJSON
    return render_template('home.html', requests=citasJSON)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
