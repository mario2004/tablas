from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tablas.db'

db = SQLAlchemy(app)

# Inicio NOTA. Este fragmento estaba en el fichero models.py y se ponía aquí un import models.py. No se sabe por qué así no funciona y no reconoce User.
from datetime import datetime

class Message(db.Model):
    idMessage = db.Column(db.Integer, primary_key=True)
    idAppointment = db.Column(db.Integer, db.ForeignKey('appointment.idAppointment'), nullable=False)
    idUserReceiver = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    idUserSender = db.Column(db.Integer, nullable=False)
    messageDate = db.Column(db.DateTime, nullable=False, default=datetime.now)
    messageText = db.Column(db.Text, unique=True, nullable=False)
    # Relación de muchos a uno con la tabla Appointment
    # appointment = db.relationship("Appointment", back_populates="messages")
    appointment = db.relationship('Appointment', backref=db.backref('messages', lazy=True))
    user = db.relationship('User', backref=db.backref('users', lazy=True))
    def to_dict(self):
        return {
            'idMessage': self.idMessage,
            'idAppointment': self.idAppointment,
            'idUserReceiver': self.idUserReceiver,
            'idUserSender': self.idUserSender,
            'messageDate': self.messageDate.isoformat() if self.messageDate else '',
            'messageText': self.messageText,
            'appointment': self.appointment.to_dict(),
            'user': self.user.to_dict()
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
            # No incluimos el password_hash por seguridad
        }

class Request(db.Model):
    idRequest = db.Column(db.Integer, primary_key=True)
    idAppointment = db.Column(db.Integer, db.ForeignKey('appointment.idAppointment'), nullable=False)
    idUser = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    idUserSender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    requestText = db.Column(db.Text, unique=True, nullable=True)
    accepted = db.Column(db.Boolean, nullable=False, default=False)
    appointment = db.relationship('Appointment', backref=db.backref('requests', lazy=True))
    def to_dict(self):
        return {
            'idRequest': self.idRequest,
            'idAppointment': self.idAppointment,
            'idUser': self.idUser,
            'idUserSender': self.idUserSender,
            'requestText': self.requestText,
            'accepted': json.dumps(self.accepted),
            'appointment': self.appointment.to_dict()
        }

class Appointment(db.Model):
    idAppointment = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    appointmentDate = db.Column(db.DateTime, nullable=False, default=datetime.now)
    place = db.Column(db.String(200), nullable=False)
    currencyFrom = db.Column(db.String(10), nullable=False)
    currencyTo = db.Column(db.String(10), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    reserved=db.Column(db.Boolean, nullable=False, default=False)
    user = db.relationship('User', backref=db.backref('appointments', lazy=True))
    # Relación de uno a muchos con la tabla Message
    # Explicado aquí https://medium.com/@kimberlymlove15/sqlalchemy-relationship-status-its-complicated-backref-vs-back-populates-9eaf07335a13
    # messages = db.relationship("Message", back_populates="appointment")
    def to_dict(self):
        return {
            'idAppointment': self.idAppointment,
            'idUser': self.idUser,
            'amount': self.amount,
            'appointmentDate': self.appointmentDate.isoformat() if self.appointmentDate else '',
            'place': self.place,
            'currencyFrom': self.currencyFrom,
            'currencyTo': self.currencyTo,
            'lat': self.lat,
            'lon': self.lon,
            'reserved': json.dumps(self.reserved),
            'user': self.user.to_dict()  # Incluye los detalles del usuario
        }


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    s = db.session()
    messagesDB = s.query(Message).all()
    messagesJSON=[message.to_dict() for message in messagesDB]
    return render_template('home.html', messages=messagesJSON)
    
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
