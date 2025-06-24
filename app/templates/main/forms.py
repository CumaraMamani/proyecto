from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class RoomForm(FlaskForm):
    room_number = StringField('Número de Habitación', validators=[DataRequired()])
    room_type = SelectField('Tipo', choices=[('simple', 'Simple'), ('doble', 'Doble'), ('suite', 'Suite')], validators=[DataRequired()])
    
    # Usamos DecimalField para los precios con precisión
    price = DecimalField('Precio', places=2, validators=[DataRequired(), NumberRange(min=0)])

    # ✅ NUEVO CAMPO DE ESTADO
    status = SelectField('Estado', choices=[
        ('Disponible', 'Disponible'),
        ('Ocupada', 'Ocupada'),
        ('Mantenimiento', 'Mantenimiento')
    ], validators=[DataRequired()])

    submit = SubmitField('Guardar')
