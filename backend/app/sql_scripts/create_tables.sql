-- 创建用户表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL, -- 明文密码
    role VARCHAR(20) NOT NULL      -- 用户角色（admin, doctor, patient）
);

-- 创建科室表
CREATE TABLE Departments (
    id SERIAL PRIMARY KEY,  -- 科室 ID
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(15) NOT NULL
);

-- 创建医生表
CREATE TABLE Doctors (
    id SERIAL PRIMARY KEY,  -- 医生 ID
    name VARCHAR(255) NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F')) NOT NULL,
    age INT CHECK (age > 0 AND age < 120) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    specialization VARCHAR(255) NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES Departments (id) ON DELETE CASCADE
);

-- 创建患者表
CREATE TABLE Patients (
    id SERIAL PRIMARY KEY,  -- 患者 ID
    name VARCHAR(255) NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F')) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    primary_doctor_id INT,
    FOREIGN KEY (primary_doctor_id) REFERENCES Doctors (id) ON DELETE SET NULL
);

-- 创建挂号表
CREATE TABLE Registrations (
    id SERIAL PRIMARY KEY,  -- 挂号 ID
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    department_id INT NOT NULL,
    registration_date DATE NOT NULL,
    visit_type VARCHAR(50) CHECK (visit_type IN ('初诊', '复诊')) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patients (id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctors (id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES Departments (id) ON DELETE CASCADE
);
