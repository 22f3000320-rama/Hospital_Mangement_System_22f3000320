from flask import current_app as app, render_template, request, redirect, url_for
from datetime import datetime
from .models import *
from flask_login import login_user, login_required, current_user

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("patient_registration.html")
    elif request.method == "POST":
        name = request.form.get("p_name")
        user_name = request.form.get("p_user_name")
        email = request.form.get("p_email")
        password = request.form.get("p_pswd")
        contact_number = request.form.get("p_contact_number")
        dob = request.form.get("p_date_of_birth")
        address = request.form.get("p_address")

        dob_obj = None
        if dob:
            try:
                dob_obj = datetime.strptime(dob, "%Y-%m-%d").date()
            except ValueError:
                return "Invalid date format! Please use YYYY-MM-DD.", 400

        patient_obj = db.session.query(Patient).filter_by(email=email).first()
        if not patient_obj:
            patient_data = Patient(full_name=name,email=email,username=user_name,password=password,contact_no=contact_number,dob=dob_obj,address=address)
            db.session.add(patient_data)
            db.session.commit()
            return redirect("/login")
        else:
            return "User already exists."

    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pswd")
        doc_obj=db.session.query(Doctor).filter_by(email=email).first()
        patient_obj=db.session.query(Patient).filter_by(email=email).first()
        admin_obj=db.session.query(Admin).filter_by(email=email).first()
        if doc_obj and doc_obj.password==password:
            login_user(doc_obj)
            return redirect("/dashboard/doc")
        elif patient_obj and patient_obj.password==password:
            login_user(patient_obj)
            return redirect("/dashboard/patient")
        elif admin_obj and admin_obj.password==password:
            login_user(admin_obj)
            return redirect("/dashboard/admin")
        else:
            return "Invalid credentials!!!"
        

@app.route("/dashboard/doc")
@login_required
def doc_dashboard():
    if isinstance(current_user, Doctor):
        return "Welcome doc!!!"
    else:
        return "Something went wrong."

@app.route("/dashboard/patient")
@login_required
def patient_dashboard():
    if isinstance(current_user, Patient):
        return "Welcome to Your Profile!!!"
    else:  
        return "Something went wrong."

@app.route("/dashboard/admin")
@login_required
def admin_dashboard():
    if isinstance(current_user, Admin):
        return "Welcome Admin!!!"
    else:
        return "Something went wrong."


        


    