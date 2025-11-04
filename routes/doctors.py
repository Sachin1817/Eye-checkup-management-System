from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db, Doctor
from forms import DoctorForm
from sqlalchemy.exc import IntegrityError

doctors_bp = Blueprint('doctors', __name__)

@doctors_bp.route('/')
def list_doctors():
    doctors = Doctor.query.all()
    return render_template('doctors/list.html', doctors=doctors)

@doctors_bp.route('/add', methods=['GET', 'POST'])
def add_doctor():
    form = DoctorForm()
    if form.validate_on_submit():
        try:
            doctor = Doctor(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                specialty=form.specialty.data,
                phone=form.phone.data,
                email=form.email.data,
                license_number=form.license_number.data
            )
            db.session.add(doctor)
            db.session.commit()
            flash('Doctor added successfully!', 'success')
            return redirect(url_for('doctors.list_doctors'))
        except IntegrityError as e:
            db.session.rollback()
            if 'license_number' in str(e).lower():
                flash('A doctor with this license number already exists. Please use a different license number.', 'error')
            elif 'email' in str(e).lower():
                flash('A doctor with this email already exists. Please use a different email.', 'error')
            else:
                flash('An error occurred while adding the doctor. Please try again.', 'error')
    return render_template('doctors/add.html', form=form)

@doctors_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    form = DoctorForm(obj=doctor)
    if form.validate_on_submit():
        form.populate_obj(doctor)
        db.session.commit()
        flash('Doctor updated successfully!', 'success')
        return redirect(url_for('doctors.list_doctors'))
    return render_template('doctors/edit.html', form=form, doctor=doctor)

@doctors_bp.route('/delete/<int:id>', methods=['POST'])
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    try:
        # Delete related prescriptions first
        for prescription in doctor.prescriptions:
            db.session.delete(prescription)

        # Delete related appointments (which will cascade to delete billings and eye_tests)
        for appointment in doctor.appointments:
            # Delete billings and eye_tests for each appointment
            for billing in appointment.billings:
                db.session.delete(billing)
            for eye_test in appointment.eye_tests:
                db.session.delete(eye_test)
            db.session.delete(appointment)

        # Delete the doctor
        db.session.delete(doctor)
        db.session.commit()
        flash('Doctor deleted successfully!', 'success')
    except IntegrityError as e:
        db.session.rollback()
        flash('Cannot delete doctor due to related records. Please remove associated data first.', 'error')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the doctor.', 'error')
    return redirect(url_for('doctors.list_doctors'))

@doctors_bp.route('/view/<int:id>')
def view_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    return render_template('doctors/view.html', doctor=doctor)
