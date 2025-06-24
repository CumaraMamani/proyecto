# app/main/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, IntegerField, SelectField
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from wtforms import SelectField

class RoomForm(FlaskForm):
    room_number = StringField('Número', validators=[DataRequired()])
    room_type = StringField('Tipo', validators=[DataRequired()])
    price = FloatField('Precio', validators=[DataRequired()])
    status = SelectField('Estado', choices=[
        ('Disponible', 'Disponible'),
        ('Ocupada', 'Ocupada'),
        ('Mantenimiento', 'Mantenimiento')
    ])
    submit = SubmitField('Guardar')

class ReservationForm(FlaskForm):
    check_in_date = DateField('Fecha de entrada', format='%Y-%m-%d', validators=[DataRequired()])
    check_out_date = DateField('Fecha de salida', format='%Y-%m-%d', validators=[DataRequired()])
    num_people = IntegerField('Número de personas', validators=[DataRequired()])
    room_type = SelectField('Tipo de habitación', choices=[
        ('Sencilla', 'Sencilla'),
        ('Doble', 'Doble'),
        ('Suite', 'Suite'),
    ], validators=[DataRequired()])
    submit = SubmitField('Reservar')


