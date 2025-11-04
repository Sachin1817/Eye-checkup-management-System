from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db, Prescription, Patient, Doctor
from forms import PrescriptionForm
from sqlalchemy.exc import IntegrityError

prescriptions_bp = Blueprint('prescriptions', __name__)

@prescriptions_bp.route('/')
def list_prescriptions():
    prescriptions = Prescription.query.all()
    return render_template('prescriptions/list.html', prescriptions=prescriptions)

@prescriptions_bp.route('/add', methods=['GET', 'POST'])
def add_prescription():
    form = PrescriptionForm()
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    form.patient_id.choices = [(p.id, f"{p.first_name} {p.last_name}") for p in patients]
    form.doctor_id.choices = [(d.id, f"{d.first_name} {d.last_name}") for d in doctors]

    if not patients:
        flash('No patients available. Please add a patient first.', 'warning')
    if not doctors:
        flash('No doctors available. Please add a doctor first.', 'warning')

    if form.validate_on_submit():
        try:
            prescription = Prescription(
                patient_id=form.patient_id.data,
                doctor_id=form.doctor_id.data,
                prescription_date=form.prescription_date.data,
                sphere_left=form.sphere_left.data,
                cylinder_left=form.cylinder_left.data,
                axis_left=form.axis_left.data,
                sphere_right=form.sphere_right.data,
                cylinder_right=form.cylinder_right.data,
                axis_right=form.axis_right.data,
                pupillary_distance=form.pupillary_distance.data,
                duration_months=form.duration_months.data,
                notes=form.notes.data
            )
            db.session.add(prescription)
            db.session.commit()
            flash('Prescription added successfully!', 'success')
            return redirect(url_for('prescriptions.list_prescriptions'))
        except IntegrityError as e:
            db.session.rollback()
            flash('Database integrity error. Please check that the patient and doctor exist.', 'error')
        except Exception as e:
            db.session.rollback()
            flash('An unexpected error occurred. Please try again.', 'error')
    else:
        # Flash form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')

    return render_template('prescriptions/add.html', form=form)

@prescriptions_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_prescription(id):
    prescription = Prescription.query.get_or_404(id)
    form = PrescriptionForm(obj=prescription)
    form.patient_id.choices = [(p.id, f"{p.first_name} {p.last_name}") for p in Patient.query.all()]
    form.doctor_id.choices = [(d.id, f"{d.first_name} {d.last_name}") for d in Doctor.query.all()]
    if form.validate_on_submit():
        form.populate_obj(prescription)
        db.session.commit()
        flash('Prescription updated successfully!', 'success')
        return redirect(url_for('prescriptions.list_prescriptions'))
    return render_template('prescriptions/edit.html', form=form, prescription=prescription)

@prescriptions_bp.route('/delete/<int:id>', methods=['POST'])
def delete_prescription(id):
    prescription = Prescription.query.get_or_404(id)
    db.session.delete(prescription)
    db.session.commit()
    flash('Prescription deleted successfully!', 'success')
    return redirect(url_for('prescriptions.list_prescriptions'))

@prescriptions_bp.route('/view/<int:id>')
def view_prescription(id):
    prescription = Prescription.query.get_or_404(id)
    return render_template('prescriptions/view.html', prescription=prescription)
