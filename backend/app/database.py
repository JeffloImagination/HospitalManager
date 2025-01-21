from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db = SQLAlchemy()

# 初始化app
def init_app(app: Flask):
    db.init_app(app)
    
    count = 0
    # 创建表
    with app.app_context():
        db.create_all()
        
        ## 下面两行代码用于调试
        count = count + 1
        print(f"HEY!!!!counttt = {count}")
        # execute_sql_script("sql_scripts/insert_departments.sql")
        # execute_sql_script("sql_scripts/insert_doctors.sql")
        # execute_sql_script("sql_scripts/insert_patients.sql")
        # execute_sql_script("sql_scripts/insert_registrations.sql")
        


def execute_sql_script(file_path):
    """执行 SQL 文件"""

    current_dir = os.path.dirname(__file__)
    sql_scripts_path = os.path.join(current_dir, file_path)

    with open(sql_scripts_path, 'r', encoding='utf-8') as file:
        sql_commands = file.read()
        # print(sql_commands)
        db.session.execute(sql_commands)
        db.session.commit()

    # with db.engine.connect() as connection:
    #     for statement in sql.split(";"):
    #         if statement.strip():
    #             connection.execute(statement)
