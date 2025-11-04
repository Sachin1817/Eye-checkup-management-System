from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db, Appointment, Patient, Doctor
from forms import AppointmentForm
from sqlalchemy.exc import IntegrityError

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/')
def list_appointments():
    appointments = Appointment.query.all()
    return render_template('appointments/list.html', appointments=appointments)

@appointments_bp.route('/add', methods=['GET', 'POST'])
def add_appointment():
    form = AppointmentForm()
    form.patient_id.choices = [(p.id, f"{p.first_name} {p.last_name}") for p in Patient.query.all()]
    form.doctor_id.choices = [(d.id, f"{d.first_name} {d.last_name}") for d in Doctor.query.all()]
    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=form.patient_id.data,
            doctor_id=form.doctor_id.data,
            appointment_date=form.appointment_date.data,
            appointment_time=form.appointment_time.data,
            status=form.status.data,
            notes=form.notes.data
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment added successfully!', 'success')
        return redirect(url_for('appointments.list_appointments'))
    return render_template('appointments/add.html', form=form)

@appointments_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    form = AppointmentForm(obj=appointment)
    form.patient_id.choices = [(p.id, f"{p.first_name} {p.last_name}") for p in Patient.query.all()]
    form.doctor_id.choices = [(d.id, f"{d.first_name} {d.last_name}") for d in Doctor.query.all()]
    if form.validate_on_submit():
        form.populate_obj(appointment)
        db.session.commit()
        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('appointments.list_appointments'))
    return render_template('appointments/edit.html', form=form, appointment=appointment)

@appointments_bp.route('/delete/<int:id>', methods=['POST'])
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    try:
        # Delete related billings first (since appointment_id is NOT NULL)
        for billing in appointment.billings:
            db.session.delete(billing)

        # Delete related eye tests (since appointment_id is NOT NULL)
        for eye_test in appointment.eye_tests:
            db.session.delete(eye_test)

        # Delete the appointment
        db.session.delete(appointment)
        db.session.commit()
        flash('Appointment deleted successfully!', 'success')
    except IntegrityError as e:
        db.session.rollback()
        flash('Cannot delete appointment due to related records. Please remove associated data first.', 'error')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the appointment.', 'error')
    return redirect(url_for('appointments.list_appointments'))

@appointments_bp.route('/view/<int:id>')
def view_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    return render_template('appointments/view.html', appointment=appointment)
