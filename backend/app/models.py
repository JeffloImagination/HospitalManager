from .database import db
from sqlalchemy import Column, Integer, String

# 定义科室类
class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

# 定义医生类
class Doctor(db.Model):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))

# 定义患者类
class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    primary_doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))

# 定义挂号类
class Registration(db.Model):
    __tablename__ = "registrations"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    registration_date = db.Column(db.Date, nullable=False)
    visit_type = db.Column(db.String(10), nullable=False)

# 定义用户类
class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    role = Column(String(20), nullable=False)
