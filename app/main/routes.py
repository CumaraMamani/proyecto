from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models.models import Reservation, Room
from app.main.forms import ReservationForm, RoomForm
from functools import wraps

# Decorador para verificar si el usuario es admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

main = Blueprint('main', __name__)

# ✅ Ruta principal (inicio)
@main.route('/')
def index():
    return render_template('main/index.html')

# -------------------- RESERVAS (usuario) --------------------

# Crear una reserva
@main.route('/reserve', methods=['GET', 'POST'])
@login_required
def reserve():
    form = ReservationForm()
    if form.validate_on_submit():
        room = Room.query.filter_by(room_type=form.room_type.data).first()
        if not room:
            flash('No hay habitaciones disponibles para ese tipo.', 'danger')
            return redirect(url_for('main.reserve'))

        new_reservation = Reservation(
            check_in_date=form.check_in_date.data,
            check_out_date=form.check_out_date.data,
            num_people=form.num_people.data,
            user_id=current_user.id,
            room_id=room.id
        )
        db.session.add(new_reservation)
        db.session.commit()
        flash('Reserva creada con éxito.', 'success')
        return redirect(url_for('main.reservations'))  # <- Usamos alias del endpoint

    return render_template('main/reserve.html', form=form)

# Ver reservas del usuario actual
@main.route('/reservations', endpoint='reservations')  # <- Alias para usar url_for('main.reservations')
@login_required
def my_reservations():
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template('main/reservations.html', reservations=reservations)

# Cancelar una reserva (usuario)
@main.route('/reservations/cancel/<int:id>', methods=['GET', 'POST'])
@login_required
def cancel_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    if reservation.user_id != current_user.id:
        flash('No tienes permiso para cancelar esta reserva.', 'danger')
        return redirect(url_for('main.reservations'))

    if reservation.status == 'Cancelada':
        flash("Esta reserva ya ha sido cancelada.", "warning")
        return redirect(url_for('main.reservations'))

    reservation.status = 'Cancelada'
    db.session.commit()
    flash('Reserva cancelada con éxito.', 'info')
    return redirect(url_for('main.reservations'))

# -------------------- HABITACIONES (admin) --------------------

# Ver todas las habitaciones
@main.route('/admin/rooms')
@login_required
@admin_required
def admin_rooms():
    rooms = Room.query.all()
    return render_template('admin/rooms.html', rooms=rooms)

# Crear nueva habitación
@main.route('/admin/rooms/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_room():
    form = RoomForm()
    if form.validate_on_submit():
        room = Room(
            room_number=form.room_number.data,
            room_type=form.room_type.data,
            price=form.price.data
        )
        db.session.add(room)
        db.session.commit()
        flash('Habitación creada exitosamente.', 'success')
        return redirect(url_for('main.admin_rooms'))
    return render_template('admin/room_form.html', form=form)

# Editar habitación
@main.route('/admin/rooms/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_room(id):
    room = Room.query.get_or_404(id)
    form = RoomForm(obj=room)
    if form.validate_on_submit():
        room.room_number = form.room_number.data
        room.room_type = form.room_type.data
        room.price = form.price.data
        db.session.commit()
        flash('Habitación actualizada.', 'success')
        return redirect(url_for('main.admin_rooms'))
    return render_template('admin/room_form.html', form=form)

# Eliminar habitación
@main.route('/admin/rooms/delete/<int:id>')
@login_required
@admin_required
def delete_room(id):
    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    flash('Habitación eliminada.', 'info')
    return redirect(url_for('main.admin_rooms'))
