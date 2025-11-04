# Eye Checkup Management System

A comprehensive web-based application for managing eye care clinic operations, built with Flask and SQLAlchemy. This system allows clinics to efficiently manage patients, doctors, appointments, eye test results, prescriptions, billing, and generate reports.

## Features

- **Patient Management**: Register and manage patient information including personal details and medical history
- **Doctor Management**: Maintain doctor profiles with specialties and license information
- **Appointment Scheduling**: Schedule, track, and manage patient appointments
- **Eye Test Results**: Record and store comprehensive eye examination results
- **Prescription Management**: Create and manage eye prescriptions with detailed parameters
- **Billing System**: Handle billing and payment tracking for services
- **Reporting**: Generate various reports for clinic analytics and patient history

## Database Models

### Patient
- Personal information (name, DOB, gender, contact details)
- Medical history tracking
- Relationships with appointments, prescriptions, billings, and eye tests

### Doctor
- Professional information (name, specialty, license)
- Contact details
- Relationships with appointments and prescriptions

### Appointment
- Links patients and doctors
- Scheduling information (date, time, status)
- Notes and tracking
- Relationships with eye tests and billings

### EyeTestResult
- Comprehensive eye examination data
- Visual acuity measurements
- Intraocular pressure readings
- Fundus examination notes
- Other clinical findings

### Prescription
- Detailed eye prescription parameters (sphere, cylinder, axis for both eyes)
- Pupillary distance measurements
- Prescription duration and notes

### Billing
- Service charges and payment tracking
- Payment status management
- Payment method recording

### Report
- Various report types for analytics
- Generation tracking and parameters
- Data storage for generated reports

## Technology Stack

### Backend
- **Flask 3.0.3**: Web framework for Python
- **Flask-SQLAlchemy 3.1.1**: ORM for database operations
- **Flask-WTF 1.2.1**: Form handling and validation
- **WTForms 3.1.2**: Form creation and validation
- **Flask-Bootstrap5**: UI framework integration

### Frontend
- **HTML5**: Markup language
- **CSS3**: Styling
- **JavaScript**: Client-side scripting
- **Bootstrap 5**: Responsive UI framework

### Database
- **SQLite**: Default database (development)
- **SQLAlchemy**: Database abstraction layer

### Additional Libraries
- **python-dotenv 1.0.1**: Environment variable management
- **email-validator 2.1.0**: Email validation

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sachin1817/Eye-checkup-management-System.git
   cd Eye-checkup-management-System
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory with:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   SQLALCHEMY_DATABASE_URI=sqlite:///eye_management.db
   ```

5. **Initialize the database:**
   ```bash
   python init_db.py
   ```

6. **Run the application:**
   ```bash
   python run.py
   ```

   The application will be available at `http://localhost:5000`

## Usage

### Patient Management
- Add new patients with complete profile information
- View and edit patient details
- Track medical history and appointment records

### Doctor Management
- Register doctors with their specialties
- Maintain license information
- View doctor schedules and appointments

### Appointment Scheduling
- Schedule appointments between patients and doctors
- Track appointment status (scheduled, completed, cancelled)
- Add appointment notes

### Eye Examinations
- Record comprehensive eye test results
- Store visual acuity and pressure measurements
- Document examination findings

### Prescriptions
- Create detailed eye prescriptions
- Specify parameters for both eyes
- Set prescription duration and notes

### Billing
- Generate bills for services
- Track payment status
- Record payment methods

### Reports
- Generate patient history reports
- Create appointment summaries
- View clinic analytics

## Project Structure

```
eye-management/
├── app.py                 # Main Flask application
├── models.py             # Database models
├── forms.py              # WTForms definitions
├── run.py                # Application runner
├── init_db.py            # Database initialization
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── instance/
│   └── eye_management.db # SQLite database
├── routes/               # Route handlers
│   ├── __init__.py
│   ├── patients.py
│   ├── doctors.py
│   ├── appointments.py
│   ├── eye_tests.py
│   ├── prescriptions.py
│   ├── billings.py
│   └── reports.py
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── patients/
│   ├── doctors/
│   ├── appointments/
│   ├── eye_tests/
│   ├── prescriptions/
│   ├── billings/
│   └── reports/
└── static/               # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email sachin@example.com or open an issue in the GitHub repository.
