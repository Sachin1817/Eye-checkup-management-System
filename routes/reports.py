from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from models import db, Report, Patient, Doctor, Appointment, Billing
from forms import ReportForm
import json
from datetime import datetime

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/')
def index():
    form = ReportForm()
    form.patient_id.choices = [(0, 'All Patients')] + [(p.id, f"{p.first_name} {p.last_name}") for p in Patient.query.all()]
    form.doctor_id.choices = [(0, 'All Doctors')] + [(d.id, f"{d.first_name} {d.last_name}") for d in Doctor.query.all()]
    return render_template('reports/index.html', form=form)

@reports_bp.route('/generate', methods=['GET', 'POST'])
def generate_report():
    form = ReportForm()
    form.patient_id.choices = [(0, 'All Patients')] + [(p.id, f"{p.first_name} {p.last_name}") for p in Patient.query.all()]
    form.doctor_id.choices = [(0, 'All Doctors')] + [(d.id, f"{d.first_name} {d.last_name}") for d in Doctor.query.all()]

    if request.method == 'POST':
        print("POST request received")
        print("Form data:", request.form)
        if form.validate_on_submit():
            print("Form validated successfully")
            print("Report type:", form.report_type.data)
            print("Start date:", form.start_date.data)
            print("End date:", form.end_date.data)
            print("Patient ID:", form.patient_id.data)
            print("Doctor ID:", form.doctor_id.data)
            report_data = {}

            if form.report_type.data == 'patient_history':
                patient_id = form.patient_id.data if form.patient_id.data != 0 else None
                query = Patient.query
                if patient_id:
                    query = query.filter_by(id=patient_id)
                patients = query.all()
                report_data = {
                    'patients': [
                        {
                            'id': p.id,
                            'name': f"{p.first_name} {p.last_name}",
                            'appointments': len(p.appointments),
                            'prescriptions': len(p.prescriptions),
                            'billings': len(p.billings)
                        } for p in patients
                    ]
                }

            elif form.report_type.data == 'appointment_summary':
                start_date = form.start_date.data
                end_date = form.end_date.data
                query = Appointment.query
                if start_date:
                    query = query.filter(Appointment.appointment_date >= start_date)
                if end_date:
                    query = query.filter(Appointment.appointment_date <= end_date)
                appointments = query.all()
                report_data = {
                    'total_appointments': len(appointments),
                    'scheduled': len([a for a in appointments if a.status == 'scheduled']),
                    'completed': len([a for a in appointments if a.status == 'completed']),
                    'cancelled': len([a for a in appointments if a.status == 'cancelled'])
                }

            elif form.report_type.data == 'billing_summary':
                start_date = form.start_date.data
                end_date = form.end_date.data
                query = Billing.query
                if start_date:
                    query = query.filter(Billing.created_at >= start_date)
                if end_date:
                    query = query.filter(Billing.created_at <= end_date)
                billings = query.all()
                total_amount = sum(b.amount for b in billings if b.status == 'paid')
                report_data = {
                    'total_billings': len(billings),
                    'paid': len([b for b in billings if b.status == 'paid']),
                    'pending': len([b for b in billings if b.status == 'pending']),
                    'total_amount': total_amount
                }

            elif form.report_type.data == 'doctor_performance':
                doctors = Doctor.query.all()
                report_data = {
                    'doctors': [
                        {
                            'id': d.id,
                            'name': f"{d.first_name} {d.last_name}",
                            'appointments': len(d.appointments),
                            'prescriptions': len(d.prescriptions)
                        } for d in doctors
                    ]
                }

            # Save report to database
            report = Report(
                report_type=form.report_type.data,
                generated_by='System User',  # In a real app, this would be the current user
                parameters=json.dumps({
                    'start_date': str(form.start_date.data) if form.start_date.data else None,
                    'end_date': str(form.end_date.data) if form.end_date.data else None,
                    'patient_id': form.patient_id.data if form.patient_id.data != 0 else None,
                    'doctor_id': form.doctor_id.data if form.doctor_id.data != 0 else None
                }),
                data=json.dumps(report_data)
            )
            db.session.add(report)
            db.session.commit()

            flash('Report generated successfully!', 'success')
            return redirect(url_for('reports.view_report', id=report.id))
        else:
            print("Form validation failed")
            print("Form errors:", form.errors)

    return render_template('reports/generate.html', form=form)

@reports_bp.route('/view/<int:id>')
def view_report(id):
    report = Report.query.get_or_404(id)
    data = json.loads(report.data)
    parameters = json.loads(report.parameters)
    return render_template('reports/view.html', report=report, data=data, parameters=parameters)

@reports_bp.route('/list')
def list_reports():
    reports = Report.query.order_by(Report.generated_at.desc()).all()
    return render_template('reports/list.html', reports=reports)

@reports_bp.route('/delete/<int:id>', methods=['POST'])
def delete_report(id):
    report = Report.query.get_or_404(id)
    try:
        db.session.delete(report)
        db.session.commit()
        flash('Report deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the report.', 'error')
    return redirect(url_for('reports.list_reports'))
