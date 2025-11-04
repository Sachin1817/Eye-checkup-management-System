from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db, Billing, Appointment, Patient
from forms import BillingForm

billings_bp = Blueprint('billings', __name__)

@billings_bp.route('/')
def list_billings():
    billings = Billing.query.all()
    return render_template('billings/list.html', billings=billings)

@billings_bp.route('/add', methods=['GET', 'POST'])
def add_billing():
    form = BillingForm()
    form.appointment_id.choices = [(0, 'No Appointment')] + [(a.id, f"Appointment {a.id} - {a.patient.first_name} {a.patient.last_name}") for a in Appointment.query.all()]
    form.patient_id.choices = [(p.id, f"{p.first_name} {p.last_name}") for p in Patient.query.all()]
    if form.validate_on_submit():
        billing = Billing(
            appointment_id=form.appointment_id.data if form.appointment_id.data != 0 else None,
            patient_id=form.patient_id.data,
            amount=form.amount.data,
            status=form.status.data,
            payment_date=form.payment_date.data,
            payment_method=form.payment_method.data,
            notes=form.notes.data
        )
        db.session.add(billing)
        db.session.commit()
        flash('Billing record added successfully!', 'success')
        return redirect(url_for('billings.list_billings'))
    return render_template('billings/add.html', form=form)

@billings_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_billing(id):
    billing = Billing.query.get_or_404(id)
    form = BillingForm(obj=billing)
    form.appointment_id.choices = [(0, 'No Appointment')] + [(a.id, f"Appointment {a.id} - {a.patient.first_name} {a.patient.last_name}") for a in Appointment.query.all()]
    form.patient_id.choices = [(p.id, f"{p.first_name} {p.last_name}") for p in Patient.query.all()]
    if form.validate_on_submit():
        billing.appointment_id = form.appointment_id.data if form.appointment_id.data != 0 else None
        billing.patient_id = form.patient_id.data
        billing.amount = form.amount.data
        billing.status = form.status.data
        billing.payment_date = form.payment_date.data
        billing.payment_method = form.payment_method.data
        billing.notes = form.notes.data
        db.session.commit()
        flash('Billing record updated successfully!', 'success')
        return redirect(url_for('billings.list_billings'))
    return render_template('billings/edit.html', form=form, billing=billing)

@billings_bp.route('/delete/<int:id>', methods=['POST'])
def delete_billing(id):
    billing = Billing.query.get_or_404(id)
    db.session.delete(billing)
    db.session.commit()
    flash('Billing record deleted successfully!', 'success')
    return redirect(url_for('billings.list_billings'))

@billings_bp.route('/view/<int:id>')
def view_billing(id):
    billing = Billing.query.get_or_404(id)
    return render_template('billings/view.html', billing=billing)
