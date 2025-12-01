from flask import current_app as app, render_template, request, redirect, url_for
from datetime import datetime, date, time, timedelta
from .models import *
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import and_, or_ 

@app.before_request
def inactive_users():
    msg = None
    if not current_user.is_authenticated and request.endpoint != "login" and request.endpoint!="register" and request.endpoint!="home":
        if(current_user.is_active == False):
            msg = "You are not allowed to access the application. Please contact administrator."
        logout_user()
        return redirect(url_for("login", msg=msg))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("patient_registration.html")
    elif request.method == "POST":
        dob = request.form.get("p_date_of_birth")
        email=request.form.get("p_email")
        dob_obj = datetime.strptime(dob, "%Y-%m-%d").date()
        
        patient_obj = db.session.query(Patient).filter_by(email=email).first()
        if not patient_obj:
            patient_data = Patient(full_name=request.form.get("p_name"),email=email,username=request.form.get("p_user_name"),password=request.form.get("p_pswd"),contact_no=request.form.get("p_contact_number"),dob=dob_obj,address=request.form.get("p_address"))
            db.session.add(patient_data)
            db.session.commit()
            return redirect("/login")
        else:
            return "User already exists."

    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        msg=request.args.get("msg")
        return render_template("login.html", msg=msg if msg else None)
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

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")
 
@app.route("/dashboard/doc")
@login_required
def doc_dashboard():
    if isinstance(current_user, Doctor):
        today = date.today()
        appointments = Appointment.query.filter(Appointment.doc_id==current_user.id,Appointment.appointment_status == "Upcoming", Appointment.date>=today).order_by(Appointment.date,Appointment.time).all()
        patients = list({(a.patient.full_name,a.patient.id) for a in appointments})
        return render_template("doctor/doctor_dash.html",appointments=appointments,patients=patients)
    else:
        return redirect("/")

@app.route("/dashboard/patient")
@login_required
def patient_dashboard():
    if isinstance(current_user, Patient):
        today = date.today()
        last_date = today + timedelta(days=6)
        departments=db.session.query(Departments).all()
        appointment_details1=Appointment.query.filter(Appointment.appointment_status == "Upcoming", Appointment.patient_id==current_user.id, Appointment.date>=today).order_by(Appointment.date,Appointment.time).all()
        appointment_details = []
        for appointment in appointment_details1:
            if appointment.date == today:
                if appointment.time <= datetime.now().time():
                    continue
            appointment_details.append(appointment)
            
        return render_template("patient/patient_dash.html",departments=departments,records=appointment_details,today=today,last_date=last_date)
    else:  
        return redirect("/")

@app.route("/dashboard/admin")
@login_required
def admin_dashboard():
    if isinstance(current_user, Admin):
        today = date.today()
        doctors = db.session.query(Doctor).all()
        patients=db.session.query(Patient).all()
        departments=db.session.query(Departments).all()
        appointment_details1=Appointment.query.filter(Appointment.appointment_status == "Upcoming", Appointment.date>=today).order_by(Appointment.date,Appointment.time).all()
        appointment_details = []
        for appointment in appointment_details1:
            if appointment.date == today:
                if appointment.time <= datetime.now().time():
                    continue
            appointment_details.append(appointment)
        return render_template("admin/admin_dash.html",doctors=doctors,patients=patients,departments=departments,records=appointment_details)
    else:
        return redirect("/")
    
@app.route("/create/doc", methods = ["GET", "POST"])
def create_doctor():
    if request.method == "GET":
        departments = db.session.query(Departments).all()
        return render_template("admin/create_doc.html", departments=departments)
    elif request.method=="POST":
        email = request.form.get("doc_email")
        doctor_obj = db.session.query(Doctor).filter_by(email=email).first()
        if not doctor_obj:
            doctor_data = Doctor(full_name=request.form.get("doc_name"),email=email,username=request.form.get("doc_user_name"),password=request.form.get("doc_pswd"),contact_no=request.form.get("doc_contact_number"),qualification=request.form.get("doc_qualification"), description=request.form.get("doc_experience"),department_id=int(request.form.get("department_id")))
            db.session.add(doctor_data)
            db.session.commit() 
            return redirect("/dashboard/admin")
        else:
            return "Doctor already exists."


@app.route("/edit/doc", methods = ["GET", "POST"])
def edit_doctor():
    doc_id=request.args.get("id")
    departments = db.session.query(Departments).all()
    doc_obj=db.get_or_404(Doctor,doc_id)
        
    if request.method == "POST":
        doc_obj.full_name=request.form.get("doc_name")
        doc_obj.password=request.form.get("doc_pswd")
        doc_obj.department_id=int(request.form.get("doc_department_id"))
        doc_obj.contact_no=request.form.get("doc_contact_number")
        doc_obj.qualification=request.form.get("doc_qualification")
        doc_obj.description=request.form.get("doc_description")
        
        db.session.commit()
        return redirect("/dashboard/admin")
    
    return render_template("admin/edit_doc.html",doctor=doc_obj,departments=departments)

@app.route("/delete/doc", methods=["GET", "POST"])
def delete_doctor():
    if request.method == "POST":
        doc_id=request.args.get("id")
        doctor=db.get_or_404(Doctor,doc_id)
        db.session.delete(doctor)
        db.session.commit()
        return redirect("/dashboard/admin")

@app.route("/blacklist/doc", methods=["GET", "POST"])
def blacklist_doc():
    if request.method == "POST":
        doc_id=request.args.get("id")
        doctor=db.get_or_404(Doctor,doc_id)
        doctor.status=not doctor.status
        db.session.commit()
        return redirect("/dashboard/admin")
    
@app.route("/edit/patient", methods = ["GET", "POST"])
def edit_patient():
    patient_id=request.args.get("id")
    p_obj=db.get_or_404(Patient,patient_id)
    
        
    if request.method == "POST":
        dob=request.form.get("p_date_of_birth")
        dob_obj=datetime.strptime(dob, "%Y-%m-%d").date()
        p_obj.full_name=request.form.get("p_name")
        p_obj.password=request.form.get("p_pswd")
        p_obj.dob = dob_obj
        p_obj.contact_no=request.form.get("p_contact_number")
        p_obj.address=request.form.get("p_address")
        
        db.session.commit()
        
        if isinstance(current_user, Admin):
            return redirect("/dashboard/admin")
        elif isinstance(current_user, Patient):
            return redirect("/dashboard/patient")
        
    back_url = None
    if isinstance(current_user, Admin):
        back_url = "/dashboard/admin"
    elif isinstance(current_user, Patient):
        back_url = "/dashboard/patient"
    return render_template("admin/edit_patient.html",p_obj=p_obj,back_url=back_url)

@app.route("/delete/patient", methods=["GET", "POST"])
def delete_patient():
    if request.method == "POST":
        p_id=request.args.get("id")
        patient=db.get_or_404(Patient,p_id)
        db.session.delete(patient)
        db.session.commit()
        return redirect("/dashboard/admin")

@app.route("/blacklist/patient", methods=["GET", "POST"])
def blacklist_patient():
    if request.method == "POST":
        p_id=request.args.get("id")
        patient=db.get_or_404(Patient,p_id)
        patient.status=not patient.status
        db.session.commit()
        return redirect("/dashboard/admin")

@app.route("/patient_history")
def patient_history():

    p_id=request.args.get("id")
    patient_name = db.session.query(Patient.full_name).filter_by(id=p_id).first()[0]
    patient_records=db.session.query(Appointment).filter(and_(Appointment.patient_id==p_id,Appointment.appointment_status=="Completed")).order_by(Appointment.date.desc(),Appointment.time.desc()).all()
    
    back_url = None
    if isinstance(current_user, Admin):
        back_url = "/dashboard/admin"
    elif isinstance(current_user, Doctor):
        back_url = "/dashboard/doc"
    elif isinstance(current_user, Patient):
        back_url = "/dashboard/patient"

    return render_template("patient/patient_history.html", back_url=back_url, records=patient_records, patient_name=patient_name)

@app.route("/add_treatment/patient", methods=["GET", "POST"])
def add_patient_treatment():
    a_id=request.args.get("appointment_id")
    appointment = Appointment.query.get(a_id)
    treatment = appointment.treatment_details
        
    if request.method == "POST":
        
        if not treatment:
            new_td = Treatment(
                    tests_done = request.form.get("tests_done"),
                    diagnosis = request.form.get("diagnosis"),
                    appointment_id = a_id,
                    prescription = request.form.get("prescription"),
                    notes = request.form.get("notes"))
            db.session.add(new_td)
            db.session.commit()
        else:
            treatment[0].tests_done = request.form.get("tests_done")
            treatment[0].diagnosis = request.form.get("diagnosis")
            treatment[0].prescription = request.form.get("prescription")
            treatment[0].notes = request.form.get("notes")
            db.session.commit()
        return redirect("/dashboard/doc")
    
    return render_template("doctor/add_treatment.html", appointment=appointment, treatment=treatment[0] if treatment else None)

@app.route("/update_appointment/patient")
def update_appointment_patient():
    a_id = request.args.get("appointment_id")
    doc_id = request.args.get("doctor_id")
    appointment = Appointment.query.get(a_id)
    
    if request.method == "GET" and request.args.get("action")=="update":
        appointment.appointment_status = "Completed"
        db.session.commit()
        return redirect("/dashboard/doc")
    
    elif request.method == "GET" and request.args.get("action")=="cancel":
        appointment.appointment_status = "Cancelled"
        appointment.booked_slot.is_active = True
        db.session.commit()
        if isinstance(current_user, Doctor):
            return redirect("/dashboard/doc")
        elif isinstance(current_user, Patient):
            return redirect("/dashboard/patient")
        elif isinstance(current_user, Admin):
            return redirect("/dashboard/admin")
        else:
            return "Something went wrong."
        

@app.route("/view/doctor")
def view_doctor():
    doc_id=request.args.get("doctor_id")
    doctor = Doctor.query.get(doc_id)

    back_url = None
    if isinstance(current_user, Admin):
        back_url = "/dashboard/admin"
    elif isinstance(current_user, Doctor):
        back_url = "/dashboard/doc"
    elif isinstance(current_user, Patient):
        back_url = "/dashboard/patient"
    return render_template("doctor/doctor_details.html", doctor=doctor,back_url=back_url)

@app.route("/view/department")
def view_department():
    department_id = request.args.get("department_id")
    department = Departments.query.get(department_id)

    back_url = None
    if isinstance(current_user, Admin):
        back_url = "/dashboard/admin"
    elif isinstance(current_user, Doctor):
        back_url = "/dashboard/doc"
    elif isinstance(current_user, Patient):
        back_url = "/dashboard/patient"
    return render_template("departments.html", department=department,back_url=back_url)



@app.route("/doc_availability")
def weekly_availability():
    doctor_id = current_user.id
    today = date.today()
    dates = [today + timedelta(days=i) for i in range(7)]

    slots_by_date = {d: [] for d in dates}
    all_slots = Doctor_Availability.query.filter(
        Doctor_Availability.doctor_id == doctor_id,
        Doctor_Availability.date.in_(dates)
    ).order_by(Doctor_Availability.date,
               Doctor_Availability.start_time).all()
    
    for slot in all_slots:
        slots_by_date[slot.date].append(slot)

    return render_template("doctor/doctor_availability.html", dates=dates,slots_by_date=slots_by_date)


@app.route('/set_availability', methods=["GET", "POST"])
def availability_form():
    if request.method == "GET":
        selected_date_str = request.args.get('date')
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        slots_str = ["08:00-12:00", "12:00-16:00", "16:00-20:00"]
        slots_by_date = db.session.query(Doctor_Availability).filter(Doctor_Availability.doctor_id==current_user.id, Doctor_Availability.date==selected_date,Doctor_Availability.start_time.in_([time(8, 0), time(12, 0), time(16,0)])).all()
        if slots_by_date:
            inactive_slots= {}
            for slot in slots_by_date:
                if slot.start_time == time(8,0):
                    inactive_slots[1] = True
                elif slot.start_time == time(12,0):
                    inactive_slots[2] = True
                elif slot.start_time == time(16,0):
                    inactive_slots[3] = True
            return render_template("doctor/set_availability_form.html",selected_date=selected_date, slots=slots_str, inactive_slots=inactive_slots)
        else:
            inactive_slots= {1:False, 2:False, 3:False}
            return render_template("doctor/set_availability_form.html",selected_date=selected_date, slots=slots_str, inactive_slots=inactive_slots)
        
    if request.method == "POST":
        doctor_id = current_user.id
        selected_date_str = request.form.get('date')
        slot_time = request.form.getlist("slot_time")
        slot_duration = int(request.form.get('slot_duration'))
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        for slot in slot_time:
            start_str, end_str = slot.split("-")
            start_time = datetime.strptime(start_str, "%H:%M")
            end_time = datetime.strptime(end_str, "%H:%M")
            current = start_time
            while current + timedelta(minutes=slot_duration) <= end_time:
                slot_end = current + timedelta(minutes=slot_duration)

                new_slot = Doctor_Availability(
                    doctor_id=doctor_id,
                    date=selected_date,
                    start_time=current.time(),
                    end_time=slot_end.time(),
                    is_active=True
                )

                db.session.add(new_slot)
                current = slot_end

        db.session.commit()
        return redirect('/doc_availability')
        

@app.route('/toggle-slot')
def toggle_slot():
    slot_id = request.args.get('slot_id')
    slot = Doctor_Availability.query.get(slot_id)
    slot.is_active = not slot.is_active
    db.session.commit()
    return redirect('/doc_availability')

@app.route("/check_availability", methods=["GET", "POST"])
def check_availability():
    if request.method=="GET":
        doc_id = request.args.get("doc_id")
        doctor=Doctor.query.get(doc_id)
        doc_name=doctor.full_name
        today = date.today()
        dates = [today + timedelta(days=i) for i in range(7)]
        slots_by_date = {d: [] for d in dates}
        all_slots1 = Doctor_Availability.query.filter(
        Doctor_Availability.doctor_id == doc_id,
        Doctor_Availability.date.in_(dates),
        ).order_by(Doctor_Availability.date,
               Doctor_Availability.start_time).all()
        back_url=None
        all_slots = []
        for slot in all_slots1:
            if slot.date == today:
                if slot.start_time <= datetime.now().time():
                    continue
            all_slots.append(slot)
        if isinstance(current_user, Admin):
            back_url = "/dashboard/admin"
        for slot in all_slots:
            slots_by_date[slot.date].append(slot)
        is_booking_allowed=False
        is_reschedule_allowed = False
        doc_avlb_id=None
        if request.args.get("action") == "reschedule":
            doc_avlb_id = request.args.get("slot_id")
            is_reschedule_allowed = True
        if isinstance(current_user, Patient):
            is_booking_allowed = True
            back_url = "/dashboard/patient"
        return render_template("patient/check_doc_availability.html",doc_avlb_id=doc_avlb_id if doc_avlb_id else None,is_reschedule_allowed=is_reschedule_allowed,back_url=back_url,is_booking_allowed=is_booking_allowed,slots_by_date=slots_by_date, dates=dates,doc_name=doc_name,doc_id=doc_id)
    elif request.method == "POST":
        slot_ids = request.form.getlist("slot_id")
        slot_ids = [int(s) for s in slot_ids]
        doc_id = request.args.get("doc_id")
        for slot in slot_ids:
            doc_availability = Doctor_Availability.query.get(slot)
            if doc_availability.is_active == True:
                doc_availability.is_active = False
                new_appointment = Appointment(
                    patient_id = current_user.id,
                    doc_id = doc_id,
                    doctor_avlb_id = slot,
                    date = doc_availability.date,
                    time = doc_availability.start_time
                    )
                db.session.add(new_appointment)
        if request.args.get("action") == "reschedule":
            
            doc_avlb_id=request.args.get("slot_id")
            doc_booked_slot=db.session.get(Doctor_Availability,doc_avlb_id)
            doc_booked_slot.appointments[0].appointment_status = "Cancelled"
            doc_booked_slot.is_active = True
                        
        db.session.commit()
        return redirect("/dashboard/patient")

@app.route("/search")
def search():
    search_query=request.args.get("query", "").strip()
    date_query=request.args.get("date_query")
    if not search_query:
        if isinstance(current_user, Admin):
            return redirect("/dashboard/admin")
        elif isinstance(current_user, Patient):
            return redirect("/dashboard/patient")
    if search_query:
        doctors = db.session.query(Doctor).join(Departments).filter(or_(Doctor.full_name.ilike(f"%{search_query}%"),Departments.name.ilike(f"%{search_query}%"))).all()
        
        patients = db.session.query(Patient).filter(or_(Patient.full_name.ilike(f"%{search_query}%"), Patient.id==search_query, Patient.email.ilike(f"%{search_query}%"))).all()
        departments = {}
        for doctor in doctors:
            if not doctor.department.name in departments:
                departments[doctor.department.name] = doctor.department
        
        departments = departments.values()
        date_available_docs=[]
        search_by_date = False
        if date_query:
            search_by_date=True
            date_obj = datetime.strptime(date_query, "%Y-%m-%d").date()
            for doctor in doctors:
                for availability in doctor.doctor_availability:
                    if availability.date==date_obj:
                        if availability.date==date.today() and availability.start_time<=datetime.now().time():
                            if availability.is_active:
                                continue   
                        date_available_docs.append(doctor)
                        break

    return render_template("admin/search.html",date_obj=date_obj if date_query else None,search_by_date=search_by_date,
                           departments=departments,date_available_docs=date_available_docs,search_query=search_query,
                           doctors=doctors,patients=patients if isinstance(current_user, Admin) else None, 
                           back_url="/dashboard/admin" if isinstance(current_user, Admin) else "/dashboard/patient")
    











    



        


    