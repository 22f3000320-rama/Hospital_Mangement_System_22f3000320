from flask import current_app as app
from .models import *
from datetime import date, time, datetime

with app.app_context():
    db.create_all()

    if db.session.query(Admin).count() == 0:
        admin1 = Admin(username= "admin",email="admin@firstpriority.com",password="admin_admin")
        db.session.add(admin1)
        db.session.commit()

    if db.session.query(Departments).count() == 0:
        dept1 = Departments(name="Pediatrics",description="Specialized in providing treatment to your infants or children with utmost care and precision they deserve.")
        dept2 = Departments(name="Orthopedics",description="Focused on helping you keep your bones and joints healthy.")
        dept3 = Departments(name="Neurology",description="One stop solution all your problems related to brain, spinal cord and nerves.")
        dept4 = Departments(name="Dermatology",description="We specialize in: Skin Treatment, Acne and Scar Revision, Laser Treatment, Skin Pigmentation and many more...")
        db.session.add_all([dept1,dept2,dept3,dept4])
        db.session.commit()


    if db.session.query(Doctor).count() == 0:
        doc1 = Doctor(username= "abha_sonakia",email="abha_sonakia@gmail.com",password="abcd",full_name="Dr. Abha Sonakia",contact_no="9865231485",department_id=1,qualification="M.B.B.S., D.N.B. (Pediatrics)",description="Dr. Abha Sonakia has an experience of 35 years (25 years as a specialist).")
        doc2 = Doctor(username= "nitika_meshram",email="nitika_meshram@gmail.com",password="efgh",full_name="Dr. Nitika Meshram",contact_no="9869685246",department_id=2,qualification="M.B.B.S., M.S. (Orthopedics)",description="Dr. Nitika Meshram has an experience of 30 years (15 years as a specialist).")
        doc3 = Doctor(username= "milind_tendulkar",email="milind_tendulkar@gmail.com",password="ijkl",full_name="Dr. Milind Tendulkar",contact_no="9869426873",department_id=3,qualification="M.B.B.S., M.D. (Medicine)",description="Dr. Milind Tendulkar has an experience of 25 years (10 years as a specialist).")
        doc4 = Doctor(username= "rajesh_shivhare",email="rajesh_shivhare@gmail.com",password="mnop",full_name="Dr. Rajesh Shivhare",contact_no="9874865471",department_id=4,qualification="M.B.B.S., M.D. (Dermatology)",description="Dr. Rajesh Shivhare has an experience of 20 years (5 years as a specialist).")
        doc5 = Doctor(username= "kanika_ahuja",email="kanika_ahuja@gmail.com",password="mnop",full_name="Dr. Kanika Ahuja",contact_no="9885265471",department_id=2,qualification="M.B.B.S., M.D. (Orthopedics)",description="Dr. Kanika Ahuja has an experience of 10 years (2 years as a specialist).")
        doc6 = Doctor(username= "raj_thakur",email="raj_thakur@gmail.com",password="mnop",full_name="Dr. Raj Thakur",contact_no="9814565471",department_id=1,qualification="M.B.B.S., M.D. (Pediatrics)",description="Dr. Raj Thakur has an experience of 12 years (3 years as a specialist).")
        db.session.add_all([doc1,doc2,doc3,doc4,doc5,doc6])
        db.session.commit()

    if db.session.query(Patient).count() == 0:
        patient1 = Patient(username= "priya_raut",email="priya_raut@gmail.com",password="abcd",full_name="Priya Raut",contact_no="7756095077",dob=date(2000, 11, 10),address="Delhi")
        patient2 = Patient(username= "tanya_bhagwani",email="tanya_bhagwani@gmail.com",password="efgh",full_name="Tanya Bhagwani",contact_no="7756095073",dob=date(1996, 12, 3),address="Mumbai")
        patient3 = Patient(username= "lata_panjwani",email="lata_panjwani@gmail.com",password="efgh",full_name="Lata Panjwani",contact_no="7142595073",dob=date(1962, 12, 3),address="Mumbai")
        patient4 = Patient(username= "nikita_tawade",email="nikita_tawade@gmail.com",password="efgh",full_name="Nikita Tawade",contact_no="7362595073",dob=date(1985, 12, 3),address="Mumbai")
        db.session.add_all([patient1,patient2,patient3,patient4])
        db.session.commit()
        
    if db.session.query(Doctor_Availability).count() == 0:
        da1=Doctor_Availability(doctor_id=5,date=date(2025, 11, 30),start_time=time(15, 00),end_time=time(15, 30),is_active=False)
        da2=Doctor_Availability(doctor_id=4,date=date(2025, 11, 25),start_time=time(19, 30),end_time=time(20, 00),is_active=False)
        db.session.add_all([da1,da2])
        db.session.commit()

    if db.session.query(Appointment).count() == 0:
        a1=Appointment(patient_id=1,doc_id=5,doctor_avlb_id=1,appointment_status="Completed",date=date(2025, 11, 30),time=time(15, 00),booked_at=datetime(2025, 11, 25, 9, 30))
        a2=Appointment(patient_id=2,doc_id=4,doctor_avlb_id=2,appointment_status="Completed",date=date(2025, 11, 25),time=time(19, 30),booked_at=datetime(2025, 11, 24, 15, 47))
        db.session.add_all([a1,a2])
        db.session.commit()
        
    if db.session.query(Treatment).count() == 0:
        t1=Treatment(appointment_id=1,diagnosis="fracture in right leg", tests_done="X-ray", prescription="Medicine A twice a day and medcine B thrice a day.", notes="Bed rest with a cast for a month. Visit after two weeks.")
        t2=Treatment(appointment_id=2,diagnosis="eczematic skin condition", tests_done="None", prescription="Apply medicine X on dry skin five times a day", notes="Apply moisturizer as many times as possible.")
        db.session.add_all([t1,t2])
        db.session.commit()

    