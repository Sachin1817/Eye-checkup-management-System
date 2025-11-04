from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, TimeField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class PatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=50)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    address = TextAreaField('Address', validators=[DataRequired()])
    medical_history = TextAreaField('Medical History')
    submit = SubmitField('Save Patient')

class DoctorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=50)])
    specialty = StringField('Specialty', validators=[DataRequired(), Length(min=1, max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    license_number = StringField('License Number', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Save Doctor')

class AppointmentForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    appointment_date = DateField('Appointment Date', validators=[DataRequired()])
    appointment_time = TimeField('Appointment Time', validators=[DataRequired()])
    status = SelectField('Status', choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled')
    notes = TextAreaField('Notes')
    submit = SubmitField('Save Appointment')

class EyeTestResultForm(FlaskForm):
    appointment_id = SelectField('Appointment', coerce=int, validators=[DataRequired()])
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    test_date = DateField('Test Date', validators=[DataRequired()])
    visual_acuity_left = StringField('Visual Acuity Left', validators=[Length(max=20)])
    visual_acuity_right = StringField('Visual Acuity Right', validators=[Length(max=20)])
    intraocular_pressure_left = FloatField('Intraocular Pressure Left', validators=[NumberRange(min=0)])
    intraocular_pressure_right = FloatField('Intraocular Pressure Right', validators=[NumberRange(min=0)])
    fundus_examination = TextAreaField('Fundus Examination')
    other_findings = TextAreaField('Other Findings')
    submit = SubmitField('Save Eye Test Result')

class PrescriptionForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    prescription_date = DateField('Prescription Date', validators=[DataRequired()])
    sphere_left = FloatField('Sphere Left')
    cylinder_left = FloatField('Cylinder Left')
    axis_left = IntegerField('Axis Left', validators=[NumberRange(min=0, max=180)])
    sphere_right = FloatField('Sphere Right')
    cylinder_right = FloatField('Cylinder Right')
    axis_right = IntegerField('Axis Right', validators=[NumberRange(min=0, max=180)])
    pupillary_distance = FloatField('Pupillary Distance', validators=[NumberRange(min=50, max=80)])
    duration_months = IntegerField('Duration (Months)', validators=[DataRequired(), NumberRange(min=1)])
    notes = TextAreaField('Notes')
    submit = SubmitField('Save Prescription')

class BillingForm(FlaskForm):
    appointment_id = SelectField('Appointment', coerce=int)
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    status = SelectField('Status', choices=[('pending', 'Pending'), ('paid', 'Paid'), ('cancelled', 'Cancelled')], default='pending')
    payment_date = DateField('Payment Date')
    payment_method = StringField('Payment Method', validators=[Length(max=50)])
    notes = TextAreaField('Notes')
    submit = SubmitField('Save Billing')

class ReportForm(FlaskForm):
    report_type = SelectField('Report Type', choices=[
        ('patient_history', 'Patient History'),
        ('appointment_summary', 'Appointment Summary'),
        ('billing_summary', 'Billing Summary'),
        ('doctor_performance', 'Doctor Performance')
    ], validators=[DataRequired()])
    start_date = DateField('Start Date')
    end_date = DateField('End Date')
    patient_id = SelectField('Patient', coerce=int)
    doctor_id = SelectField('Doctor', coerce=int)
    submit = SubmitField('Generate Report')
