from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Define la base para las clases SQLAlchemy
Base = declarative_base()

class Appointment(Base):
    """Representa una cita."""
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    subject = Column(String)
    description = Column(String)

    # Relación de uno a muchos con la tabla Message
    messages = relationship("Message", back_populates="appointment")

    def __repr__(self):
        return f"<Appointment(id={self.id}, subject='{self.subject}')>"

class Message(Base):
    """Representa un mensaje asociado a una cita."""
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    appointment_id = Column(Integer, ForeignKey('appointments.id'))

    # Relación de muchos a uno con la tabla Appointment
    appointment = relationship("Appointment", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, content='{self.content}')>"

if __name__ == '__main__':
    # Configura la conexión a la base de datos (ejemplo con SQLite en memoria)
    engine = create_engine('sqlite:///:memory:')

    # Crea las tablas en la base de datos
    Base.metadata.create_all(engine)

    from sqlalchemy.orm import sessionmaker

    # Crea una sesión para interactuar con la base de datos
    Session = sessionmaker(bind=engine)
    session = Session()

    # Crea una cita
    cita1 = Appointment(subject="Revisión médica", description="Revisión general con el doctor.")

    # Crea algunos mensajes asociados a la cita
    mensaje1 = Message(content="Hola doctor, tengo algunas preguntas.", appointment=cita1)
    mensaje2 = Message(content="¿Cuál es el horario de la cita?", appointment=cita1)
    mensaje3 = Message(content="Gracias por su ayuda.", appointment=cita1)

    # Agrega la cita y los mensajes a la sesión
    session.add(cita1)
    session.add_all([mensaje1, mensaje2, mensaje3])

    # Confirma los cambios en la base de datos
    session.commit()

    # Consulta la cita y sus mensajes asociados
    cita_recuperada = session.query(Appointment).filter_by(subject="Revisión médica").first()
    print(cita_recuperada)
    for mensaje in cita_recuperada.messages:
        print(f"- {mensaje}")

    # Consulta un mensaje y su cita asociada
    mensaje_recuperado = session.query(Message).filter_by(content="¿Cuál es el horario de la cita?").first()
    print(mensaje_recuperado)
    print(f"Cita asociada: {mensaje_recuperado.appointment}")

    # Cierra la sesión
    session.close()