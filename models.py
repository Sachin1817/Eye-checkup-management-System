from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    medical_history = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    prescriptions = db.relationship('Prescription', backref='patient', lazy=True)
    billings = db.relationship('Billing', backref='patient', lazy=True)
    eye_tests = db.relationship('EyeTestResult', backref='patient', lazy=True)

    def __repr__(self):
        return f'<Patient {self.first_name} {self.last_name}>'

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    prescriptions = db.relationship('Prescription', backref='doctor', lazy=True)

    def __repr__(self):
        return f'<Doctor {self.first_name} {self.last_name}>'

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    eye_tests = db.relationship('EyeTestResult', backref='appointment', lazy=True)
    billings = db.relationship('Billing', backref='appointment', lazy=True)

    def __repr__(self):
        return f'<Appointment {self.id} - {self.appointment_date}>'

class EyeTestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    test_date = db.Column(db.Date, nullable=False)
    visual_acuity_left = db.Column(db.String(20))
    visual_acuity_right = db.Column(db.String(20))
    intraocular_pressure_left = db.Column(db.Float)
    intraocular_pressure_right = db.Column(db.Float)
    fundus_examination = db.Column(db.Text)
    other_findings = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<EyeTestResult {self.id} - {self.test_date}>'

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    prescription_date = db.Column(db.Date, nullable=False)
    # Left eye prescription
    sphere_left = db.Column(db.Float)
    cylinder_left = db.Column(db.Float)
    axis_left = db.Column(db.Integer)
    # Right eye prescription
    sphere_right = db.Column(db.Float)
    cylinder_right = db.Column(db.Float)
    axis_right = db.Column(db.Integer)
    # Additional details
    pupillary_distance = db.Column(db.Float)
    duration_months = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Prescription {self.id} - {self.prescription_date}>'

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, cancelled
    payment_date = db.Column(db.Date)
    payment_method = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Billing {self.id} - ${self.amount}>'

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50), nullable=False)  # patient_history, appointment_summary, etc.
    generated_by = db.Column(db.String(100), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    parameters = db.Column(db.Text)  # JSON string of report parameters
    data = db.Column(db.Text)  # JSON string of report data

    def __repr__(self):
        return f'<Report {self.report_type} - {self.generated_at}>'
