from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, current_app, g
from flask_bootstrap5 import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import db, Patient, Doctor, Appointment, Billing
from routes import (
    patients_bp,
    doctors_bp,
    appointments_bp,
    eye_tests_bp,
    prescriptions_bp,
    billings_bp,
    reports_bp
)
from datetime import datetime
import os

def create_app():
    app = Flask(__name__,
               static_folder='static',
               template_folder='templates')

    # Configuration
    app.config.update(
        SECRET_KEY='your-secret-key-here',
        SQLALCHEMY_DATABASE_URI='sqlite:///eye_management.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        TEMPLATES_AUTO_RELOAD=True,
        WTF_CSRF_ENABLED=False  # Disable CSRF for testing
    )

    # Initialize extensions with app context
    with app.app_context():
        db.init_app(app)
        bootstrap = Bootstrap(app)

        # Ensure templates can access url_for
        @app.context_processor
        def inject_template_globals():
            from flask import url_for
            return dict(url_for=url_for)

        # Create database tables
        db.create_all()

    # Add template context processors
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    @app.context_processor
    def utility_processor():
        def format_currency(amount):
            if amount is None:
                return '$0.00'
            return '${:,.2f}'.format(amount)

        def format_date(date, format='%Y-%m-%d'):
            if date is None:
                return ''
            return date.strftime(format)

        return dict(
            format_currency=format_currency,
            format_date=format_date
        )

    # Register blueprints
    app.register_blueprint(patients_bp, url_prefix='/patients')
    app.register_blueprint(doctors_bp, url_prefix='/doctors')
    app.register_blueprint(appointments_bp, url_prefix='/appointments')
    app.register_blueprint(eye_tests_bp, url_prefix='/eye_tests')
    app.register_blueprint(prescriptions_bp, url_prefix='/prescriptions')
    app.register_blueprint(billings_bp, url_prefix='/billings')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    # Test route to check template rendering
    @app.route('/test')
    def test():
        return "Test route is working!"

    return app

# Create the application instance
app = create_app()

@app.route('/')
def index():
    try:
        # Dashboard with statistics
        patient_count = Patient.query.count()
        doctor_count = Doctor.query.count()
        appointment_count = Appointment.query.count()
        billing_total = db.session.query(db.func.sum(Billing.amount)).filter(Billing.status == 'paid').scalar() or 0

        # Get recent activities (last 5 of each type)
        recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(3).all()
        recent_billings = Billing.query.order_by(Billing.created_at.desc()).limit(3).all()
        recent_patients = Patient.query.order_by(Patient.created_at.desc()).limit(3).all()

        # Combine and sort all recent activities
        activities = []

        for apt in recent_appointments:
            activities.append({
                'type': 'appointment',
                'description': f"Appointment scheduled for {apt.patient.first_name} {apt.patient.last_name}",
                'date': apt.created_at,
                'url': url_for('appointments.view_appointment', id=apt.id)
            })

        for bill in recent_billings:
            activities.append({
                'type': 'billing',
                'description': f"Billing created for {bill.patient.first_name} {bill.patient.last_name} - ${bill.amount}",
                'date': bill.created_at,
                'url': url_for('billings.view_billing', id=bill.id)
            })

        for pat in recent_patients:
            activities.append({
                'type': 'patient',
                'description': f"New patient registered: {pat.first_name} {pat.last_name}",
                'date': pat.created_at,
                'url': url_for('patients.view_patient', id=pat.id)
            })

        # Sort activities by date (most recent first)
        activities.sort(key=lambda x: x['date'], reverse=True)
        recent_activities = activities[:5]  # Take top 5 most recent

        return render_template('index.html',
                            patient_count=patient_count,
                            doctor_count=doctor_count,
                            appointment_count=appointment_count,
                            billing_total=billing_total,
                            recent_activities=recent_activities)
    except Exception as e:
        app.logger.error(f"Error in index route: {str(e)}")
        return render_template('error.html', error="An error occurred while loading the dashboard."), 500

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating database tables: {str(e)}")
    app.run(debug=True, port=5001)
