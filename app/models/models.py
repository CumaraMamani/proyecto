from app import db
from flask_login import UserMixin
from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash

# Definir los estados de la reserva como Enum
class ReservationStatus(Enum):
    PENDING = "Pendiente"
    CONFIRMED = "Confirmada"
    CANCELLED = "Cancelada"

# Modelo de Usuario
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='usuario')  # usuario o admin

    reservations = db.relationship('Reservation', back_populates='user')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Modelo de Reserva
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    num_people = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default=ReservationStatus.PENDING.value)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='reservations')

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    room = db.relationship('Room', back_populates='reservations')

    def __repr__(self):
        return f'<Reservation {self.id} for {self.user.username}>'

# Modelo de Habitación
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    reservations = db.relationship('Reservation', back_populates='room')

    def __repr__(self):
        return f'<Room {self.room_number} ({self.room_type})>'
