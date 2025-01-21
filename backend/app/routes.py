from flask import Blueprint, jsonify, request
from .models import Department, Doctor, Patient, Registration
from .database import db

api = Blueprint("api", __name__)

# 用户角色和密码存储（简单的硬编码实现）
USER_CREDENTIALS = {
    "gyj" : {"password": "lxhaigyj", "role": "admin" },
    "admin": {"password": "admin123", "role": "admin"},
    "doctor1": {"password": "doc123", "role": "doctor"},
    "patient1": {"password": "pat123", "role": "patient"}
}

# 登录接口
@api.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # 验证用户是否存在
    if username not in USER_CREDENTIALS:
        return jsonify({"error": "用户名或密码错误"}), 401

    # 验证密码是否正确
    user_info = USER_CREDENTIALS[username]
    if user_info["password"] != password:
        return jsonify({"error": "用户名或密码错误"}), 401

    # 登录成功，返回角色信息
    return jsonify({
        "message": "登录成功",
        "username": username,
        "role": user_info["role"]
    }), 200


# 统一的分页工具函数
def paginate_query(query, page, per_page):
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": pagination.items,
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page
    }


# 用于查询科室表的所有数据
@api.route('/departments', methods=['GET'])
def get_departments():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # 查询科室数据
    query = Department.query
    result = paginate_query(query, page, per_page)

    # 返回数据
    departments = [
        {
            "id": department.id,
            "name": department.name,
            "phone": department.phone
        } for department in result["items"]
    ]
    return jsonify({
        "departments": departments,
        "total": result["total"],
        "page": result["page"],
        "per_page": result["per_page"]
    })

# 用于查询医生表的所有数据
@api.route("/doctors", methods=["GET"])
def get_doctors():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # 查询医生数据
    query = Doctor.query
    result = paginate_query(query, page, per_page)

    # 返回数据
    doctors = [
        {
            "id": doctor.id,
            "name": doctor.name,
            "gender": doctor.gender,
            "age": doctor.age,
            "phone": doctor.phone,
            "specialization": doctor.specialization,
            "department_name": Department.query.get(doctor.department_id).name if doctor.department_id else None
        } for doctor in result["items"]
    ]
    return jsonify({
        "doctors": doctors,
        "total": result["total"],
        "page": result["page"],
        "per_page": result["per_page"]
    })

# 用于查询患者表的所有数据
@api.route('/patients', methods=['GET'])
def get_patients():
    page = request.args.get('page', default=1, type=int)  # 当前页数，默认为1
    per_page = request.args.get('per_page', default=10, type=int)  # 每页数量，默认为10

    # 分页查询
    patients_query = db.session.query(
        Patient.id,
        Patient.name,
        Patient.gender,
        Patient.phone,
        Doctor.name.label("doctor_name")
    ).join(Doctor, Patient.primary_doctor_id == Doctor.id)

    total = patients_query.count()  # 总记录数
    patients = patients_query.offset((page - 1) * per_page).limit(per_page).all()  # 获取分页数据

    # 格式化结果
    result = [
        {
            "id": patient.id,
            "name": patient.name,
            "gender": patient.gender,
            "phone": patient.phone,
            "doctor_name": patient.doctor_name
        }
        for patient in patients
    ]

    return jsonify({
        "patients": result,
        "total": total,
        "page": page,
        "per_page": per_page
    })


# 用于查询挂号表的所有数据
@api.route("/registrations", methods=["GET"])
def get_registrations():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # 查询挂号数据
    query = Registration.query
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    registrations = [
        {
            "id": reg.id,
            "patient_name": Patient.query.get(reg.patient_id).name if reg.patient_id else None,
            "doctor_name": Doctor.query.get(reg.doctor_id).name if reg.doctor_id else None,
            "department_name": Department.query.get(reg.department_id).name if reg.department_id else None,
            "registration_date": reg.registration_date.strftime("%Y-%m-%d"),
            "visit_type": reg.visit_type,
        }
        for reg in pagination.items
    ]

    return jsonify({
        "registrations": registrations,
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page
    })

# 用于测试数据库连接
@api.route("/test-db")
def test_db():
    try:
        with db.engine.connect() as connection:
            connection.execute("SELECT 1")
            print("DB CONNECT SUCCESSFULLLLY!!!")
        return jsonify({"message": "Database connection successful!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/')
def hello():
    return "Hello"

# 获取每个表单的总数
@api.route('/stats', methods=['GET'])
def get_stats():
    departments_count = db.session.query(Department).count()
    doctors_count = db.session.query(Doctor).count()
    patients_count = db.session.query(Patient).count()
    registrations_count = db.session.query(Registration).count()

    return jsonify({
        "departments": departments_count,
        "doctors": doctors_count,
        "patients": patients_count,
        "registrations": registrations_count
    })

# 用于添加患者
@api.route('/patients', methods=['POST'])
def add_patient():
    try:
        data = request.json

        # 检查是否提供了患者 ID
        if "id" not in data or not data["id"]:
            import random
            # 动态生成一个未使用的 7 位数字 ID
            existing_ids = {p.id for p in db.session.query(Patient.id).all()}
            while True:
                new_id = f"{random.randint(1, 9999999):07d}"  # 生成7位数ID
                if new_id not in existing_ids:
                    break
            data["id"] = new_id

        # 创建新患者
        new_patient = Patient(
            id=data["id"],
            name=data["name"],
            gender=data["gender"],
            phone=data["phone"],
            primary_doctor_id=data["primary_doctor_id"],
        )

        db.session.add(new_patient)
        db.session.commit()

        return jsonify({"message": "患者添加成功！", "id": data["id"]}), 201

    except Exception as e:
        # 打印错误日志
        print("添加患者时出错:", str(e))
        return jsonify({"error": "添加患者失败，请检查数据！", "details": str(e)}), 400

# 用于添加医生
@api.route('/doctors', methods=['POST'])
def add_doctor():
    data = request.json
    try:
        new_doctor = Doctor(
            id=data['id'],
            name=data['name'],
            gender=data['gender'],
            age=data['age'],
            phone=data['phone'],
            specialization=data['specialization'],
            department_id=data['department_id'],
        )
        db.session.add(new_doctor)
        db.session.commit()
        return jsonify({"message": "医生添加成功！"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "医生添加失败！", "error": str(e)}), 400

# 添加科室
@api.route('/departments', methods=['POST'])
def add_department():
    try:
        data = request.json

        # 验证数据
        if not data.get("name") or not data.get("phone"):
            return jsonify({"error": "缺少必要字段：name 或 phone"}), 400

        # 创建新科室
        new_department = Department(
            id=data["id"],
            name=data["name"],
            phone=data["phone"]
        )

        db.session.add(new_department)
        db.session.commit()

        return jsonify({"message": "科室添加成功！", "department_id": new_department.id}), 201

    except Exception as e:
        print("添加科室时出错:", str(e))
        return jsonify({"error": "添加科室失败", "details": str(e)}), 500


# 添加挂号信息
@api.route('/registrations', methods=['POST'])
def add_registration():
    try:
        data = request.json

        # 检查必要字段是否存在
        if not all(key in data for key in ["patient_id", "doctor_id", "department_id", "registration_date"]):
            return jsonify({"error": "缺少必要字段"}), 400

        # 检查是否提供了挂号单 ID
        if "id" not in data or not data["id"]:
            import random
            # 动态生成一个未使用的 8 位数字 ID
            existing_ids = {r.id for r in db.session.query(Registration.id).all()}
            while True:
                new_id = f"{random.randint(1, 99999999):08d}"  # 生成8位数ID
                if new_id not in existing_ids:
                    break
            data["id"] = new_id

        # 创建挂号记录
        new_registration = Registration(
            id=data["id"],
            patient_id=data["patient_id"],
            doctor_id=data["doctor_id"],
            department_id=data["department_id"],
            registration_date=data["registration_date"],
            visit_type=data["visit_type"]
        )

        db.session.add(new_registration)
        db.session.commit()

        return jsonify({"message": "挂号成功！", "registration_id": new_registration.id}), 201

    except Exception as e:
        print("添加挂号时出错:", str(e))
        return jsonify({"error": "添加挂号失败", "details": str(e)}), 500


# 删除挂号记录
@api.route('/registrations/<int:registration_id>', methods=['DELETE'])
def delete_registration(registration_id):
    try:
        # 查找挂号记录
        registration = db.session.query(Registration).filter_by(id=registration_id).first()
        if not registration:
            return jsonify({"error": "挂号记录不存在"}), 404

        # 删除挂号记录
        db.session.delete(registration)
        db.session.commit()

        return jsonify({"message": "挂号记录已删除"}), 200

    except Exception as e:
        print("删除挂号时出错:", str(e))
        return jsonify({"error": "删除挂号失败", "details": str(e)}), 500

# 删除科室
@api.route('/departments/<int:department_id>', methods=['DELETE'])
def delete_department(department_id):
    try:
        # 查找科室记录
        department = db.session.query(Department).filter_by(id=department_id).first()
        if not department:
            return jsonify({"error": "科室记录不存在"}), 404

        # 删除科室记录
        db.session.delete(department)
        db.session.commit()

        return jsonify({"message": "科室已删除"}), 200

    except Exception as e:
        print("删除科室时出错:", str(e))
        return jsonify({"error": "删除科室失败", "details": str(e)}), 500

# 删除患者记录
@api.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    try:
        # 查找患者记录
        patient = db.session.query(Patient).filter_by(id=patient_id).first()
        if not patient:
            return jsonify({"error": "患者记录不存在"}), 404

        # 删除患者记录
        db.session.delete(patient)
        db.session.commit()

        return jsonify({"message": "患者已删除"}), 200

    except Exception as e:
        print("删除患者时出错:", str(e))
        return jsonify({"error": "删除患者失败", "details": str(e)}), 500

# 删除医生记录
@api.route('/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    try:
        # 查找医生记录
        doctor = db.session.query(Doctor).filter_by(id=doctor_id).first()
        if not doctor:
            return jsonify({"error": "医生记录不存在"}), 404

        # 删除医生记录
        db.session.delete(doctor)
        db.session.commit()

        return jsonify({"message": "医生已删除"}), 200

    except Exception as e:
        print("删除科室时出错:", str(e))
        return jsonify({"error": "删除医生失败", "details": str(e)}), 500
