from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db, Patient
from forms import PatientForm
from sqlalchemy.exc import IntegrityError

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/')
def list_patients():
    patients = Patient.query.all()
    return render_template('patients/list.html', patients=patients)

@patients_bp.route('/add', methods=['GET', 'POST'])
def add_patient():
    form = PatientForm()
    if form.validate_on_submit():
        try:
            patient = Patient(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                date_of_birth=form.date_of_birth.data,
                gender=form.gender.data,
                phone=form.phone.data,
                email=form.email.data,
                address=form.address.data,
                medical_history=form.medical_history.data
            )
            db.session.add(patient)
            db.session.commit()
            flash('Patient added successfully!', 'success')
            return redirect(url_for('patients.list_patients'))
        except IntegrityError as e:
            db.session.rollback()
            if 'email' in str(e).lower():
                flash('A patient with this email already exists. Please use a different email.', 'error')
            else:
                flash('An error occurred while adding the patient. Please try again.', 'error')
    return render_template('patients/add.html', form=form)

@patients_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    form = PatientForm(obj=patient)
    if form.validate_on_submit():
        form.populate_obj(patient)
        db.session.commit()
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('patients.list_patients'))
    return render_template('patients/edit.html', form=form, patient=patient)

@patients_bp.route('/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    try:
        # Delete related prescriptions first
        for prescription in patient.prescriptions:
            db.session.delete(prescription)

        # Delete related appointments (which will cascade to delete billings and eye_tests)
        for appointment in patient.appointments:
            # Delete billings and eye_tests for each appointment
            for billing in appointment.billings:
                db.session.delete(billing)
            for eye_test in appointment.eye_tests:
                db.session.delete(eye_test)
            db.session.delete(appointment)

        # Delete the patient
        db.session.delete(patient)
        db.session.commit()
        flash('Patient deleted successfully!', 'success')
    except IntegrityError as e:
        db.session.rollback()
        flash('Cannot delete patient due to related records. Please remove associated data first.', 'error')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the patient.', 'error')
    return redirect(url_for('patients.list_patients'))

@patients_bp.route('/view/<int:id>')
def view_patient(id):
    patient = Patient.query.get_or_404(id)
    return render_template('patients/view.html', patient=patient)
