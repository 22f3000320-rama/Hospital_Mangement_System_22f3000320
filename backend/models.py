from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    status = db.Column(db.Boolean,default=True) 
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
    doctor_availability = db.relationship("Doctor_Availability",backref="doctor")
    def get_id(self):
        return self.email

class Departments(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, unique = True)
    description = db.Column(db.Text)
    doctors = db.relationship("Doctor", backref = "department")
    
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
    appointments = db.relationship("Appointment",backref="patient")
    def get_id(self):
        return self.email

class Appointment(db.Model):
    __tablename__ = "appointment"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    patient_id = db.Column(db.Integer,db.ForeignKey("patient.id"))
    doc_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))
    avlb_slot_id = db.Column(db.Integer,db.ForeignKey("doctor_availability.id"),unique=True)
    appointment_status = db.Column(db.String)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    reason_of_visit = db.Column(db.Text)
    booked_at = db.Column(db.DateTime)
    treatment_details = db.relationship("Treatment",backref="appointment_details")

class Doctor_Availability(db.Model):
    __tablename__="doctor_availability"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    is_booked = db.Column(db.Boolean)
    appointments = db.relationship("Appointment",backref="avlb_slot")

class Treatment(db.Model):
    __tablename__ = "treatment"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"))
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)      
    date_recorded = db.Column(db.DateTime)

    








