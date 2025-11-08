from flask import current_app as app
from .models import *

with app.app_context():
    db.create_all()

    if db.session.query(Admin).count() == 0:
        admin1 = Admin(username= "rama_notani",email="rama_notani@gmail.com",password="R@ma_Notani")
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
        doc1 = Doctor(username= "abha_sonakia",email="abha_sonakia@gmail.com",password="abcd",department_id=1)
        doc2 = Doctor(username= "nitika_meshram",email="nitika_meshram@gmail.com",password="efgh",department_id=2)
        doc3 = Doctor(username= "milind_tendulkar",email="milind_tendulkar@gmail.com",password="ijkl",department_id=3)
        doc4 = Doctor(username= "rajesh_shivhare",email="rajesh_shivhare@gmail.com",password="mnop",department_id=4)
        db.session.add_all([doc1,doc2,doc3,doc4])
        db.session.commit()

    if db.session.query(Patient).count() == 0:
        patient1 = Patient(username= "priya_raut",email="priya_raut@gmail.com",password="abcd")
        patient2 = Patient(username= "tanya_bhagwani",email="tanya_bhagwani@gmail.com",password="efgh")
        db.session.add_all([patient1,patient2])
        db.session.commit()

    