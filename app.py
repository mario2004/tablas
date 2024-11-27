from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # O cualquier URI de base de datos SQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Clase Appointment
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requests = db.relationship('Request', backref='appointment', lazy='dynamic')
    amount = db.Column(db.Float, nullable=False)
    appointmentDate = db.Column(db.DateTime, nullable=False, default=datetime.now)
    place = db.Column(db.String(200), nullable=False)
    currencyFrom = db.Column(db.String(10), nullable=False)
    currencyTo = db.Column(db.String(10), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    reserved=db.Column(db.Boolean, nullable=False, default=False)

class Request(db.Model):
    idRequest = db.Column(db.Integer, primary_key=True)
    requestDate = db.Column(db.DateTime, nullable=False, default=datetime.now)
    requestText = db.Column(db.Text, unique=True, nullable=True)
    appointment_id =  db.Column(db.Integer, db.ForeignKey('appointment.id'))

def get_appointments():
    citas = Appointment.query.all()
    return citas

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    citas = get_appointments()
    for cita in citas:
        print(cita.idAppointment)
