from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String) 
    def get_id(self):
        return self.email

class Doctor(db.Model,UserMixin):
    __tablename__ = "doctor"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    full_name = db.Column(db.String)
    contact_no = db.Column(db.String)
    status = db.Column(db.Boolean,default=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    appointments = db.relationship("Appointment",backref="doctor")
    doctor_availability = db.relationship("Doctor_Availability",backref="doctor",cascade="all, delete-orphan")
    qualification= db.Column(db.Text)
    description= db.Column(db.Text)
    def get_id(self):
        return self.email
    @property
    def is_active(self):
        return self.status

class Departments(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, unique = True)
    description = db.Column(db.Text)
    doctors = db.relationship("Doctor", backref = "department",cascade="all, delete-orphan")
    
class Patient(db.Model,UserMixin):
    __tablename__ = "patient"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    full_name = db.Column(db.String)
    contact_no = db.Column(db.String)
    dob = db.Column(db.Date)
    address = db.Column(db.Text)
    status = db.Column(db.Boolean,default=True)
    appointments = db.relationship("Appointment",backref="patient",cascade="all, delete-orphan")
    def get_id(self):
        return self.email
    @property
    def is_active(self):
        return self.status
    
class Doctor_Availability(db.Model):
    __tablename__="doctor_availability"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_active=db.Column(db.Boolean,nullable=False)
    appointments = db.relationship("Appointment",backref="booked_slot",cascade="all, delete-orphan")

class Appointment(db.Model):
    __tablename__ = "appointment"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    patient_id = db.Column(db.Integer,db.ForeignKey("patient.id"))
    doc_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))
    doctor_avlb_id = db.Column(db.Integer,db.ForeignKey("doctor_availability.id"))
    appointment_status = db.Column(db.String, default="Upcoming")
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    booked_at = db.Column(db.DateTime, default = datetime.now())
    treatment_details = db.relationship("Treatment",backref="appointment_details",cascade="all, delete-orphan")

class Treatment(db.Model):
    __tablename__ = "treatment"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"))
    tests_done = db.Column(db.String)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)      

    








