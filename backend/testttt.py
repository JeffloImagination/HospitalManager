'''
只是一开始用来测试的，不用管他
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# # PostgreSQL 数据库连接字符串
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hospital_admin:1234@localhost/hospital_db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁用对象修改追踪

db = SQLAlchemy(app)

# # 定义一个数据库模型
# class Patient(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     age = db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         return f'<Patient {self.name}>'

# # --------------------------------------------
# 创建数据库表
# with app.app_context():
#     db.create_all()

# from flask import jsonify, request

# @app.route('/patients', methods=['GET'])
# def get_patients():
#     patients = Patient.query.all()  # 获取所有患者数据
#     return jsonify([{'id': p.id, 'name': p.name, 'age': p.age} for p in patients])

# @app.route('/patients', methods=['POST'])
# def add_patient():
#     data = request.get_json()
#     new_patient = Patient(name=data['name'], age=data['age'])
#     db.session.add(new_patient)
#     db.session.commit()
#     return jsonify({'message': 'Patient added successfully'}), 201

# # ---------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
