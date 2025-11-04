from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db, EyeTestResult, Appointment, Patient
from forms import EyeTestResultForm
from sqlalchemy.exc import IntegrityError

eye_tests_bp = Blueprint('eye_tests', __name__)

@eye_tests_bp.route('/')
def list_eye_tests():
    eye_tests = EyeTestResult.query.all()
    return render_template('eye_tests/list.html', eye_tests=eye_tests)

@eye_tests_bp.route('/add', methods=['GET', 'POST'])
def add_eye_test():
    form = EyeTestResultForm()
    appointments = Appointment.query.all()
    patients = Patient.query.all()
    form.appointment_id.choices = [(a.id, f"Appointment {a.id} - {a.patient.first_name} {a.patient.last_name}") for a in appointments]
    form.patient_id.choices = [(p.id, f"{p.first_name} {p.last_name}") for p in patients]

    if not appointments:
        flash('No appointments available. Please create an appointment first.', 'warning')
    if not patients:
        flash('No patients available. Please add a patient first.', 'warning')

    if form.validate_on_submit():
        try:
            eye_test = EyeTestResult(
                appointment_id=form.appointment_id.data,
                patient_id=form.patient_id.data,
                test_date=form.test_date.data,
                visual_acuity_left=form.visual_acuity_left.data,
                visual_acuity_right=form.visual_acuity_right.data,
                intraocular_pressure_left=form.intraocular_pressure_left.data,
                intraocular_pressure_right=form.intraocular_pressure_right.data,
                fundus_examination=form.fundus_examination.data,
                other_findings=form.other_findings.data
            )
            db.session.add(eye_test)
            db.session.commit()
            flash('Eye test result added successfully!', 'success')
            return redirect(url_for('eye_tests.list_eye_tests'))
        except IntegrityError as e:
            db.session.rollback()
            flash('Database integrity error. Please check that the appointment and patient exist.', 'error')
        except Exception as e:
            db.session.rollback()
            flash('An unexpected error occurred. Please try again.', 'error')
    else:
        # Flash form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')

    return render_template('eye_tests/add.html', form=form)

@eye_tests_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_eye_test(id):
    eye_test = EyeTestResult.query.get_or_404(id)
    form = EyeTestResultForm(obj=eye_test)
    form.appointment_id.choices = [(a.id, f"Appointment {a.id} - {a.patient.first_name} {a.patient.last_name}") for a in Appointment.query.all()]
    form.patient_id.choices = [(p.id, f"{p.first_name} {p.last_name}") for p in Patient.query.all()]
    if form.validate_on_submit():
        form.populate_obj(eye_test)
        db.session.commit()
        flash('Eye test result updated successfully!', 'success')
        return redirect(url_for('eye_tests.list_eye_tests'))
    return render_template('eye_tests/edit.html', form=form, eye_test=eye_test)

@eye_tests_bp.route('/delete/<int:id>', methods=['POST'])
def delete_eye_test(id):
    eye_test = EyeTestResult.query.get_or_404(id)
    db.session.delete(eye_test)
    db.session.commit()
    flash('Eye test result deleted successfully!', 'success')
    return redirect(url_for('eye_tests.list_eye_tests'))

@eye_tests_bp.route('/view/<int:id>')
def view_eye_test(id):
    eye_test = EyeTestResult.query.get_or_404(id)
    return render_template('eye_tests/view.html', eye_test=eye_test)
