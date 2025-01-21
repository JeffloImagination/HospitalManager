'''
配置文件
'''

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # PostgreSQL 数据库连接字符串
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hospital_admin:1234@localhost/hospital_db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁用对象修改追踪

# import os

# class Config:
#     """基础配置类"""
#     SQLALCHEMY_DATABASE_URI = os.getenv(
#         key='DATABASE_URL', 
#         default='postgresql://hospital_admin:1234@localhost/hospital_db'
#     )  # 从环境变量读取连接字符串，默认为你的数据库配置
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')  # 用于应用的安全配置（如会话）

# class DevelopmentConfig(Config):
#     """开发环境配置"""
#     DEBUG = True

# class ProductionConfig(Config):
#     """生产环境配置"""
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # 必须设置环境变量

import os

class Config:
    SQLALCHEMY_DATABASE_URI =  'postgresql://hospital_admin:1234@localhost:5432/hospital_db' # 'postgresql://用户名:密码@localhost:运行端口(postgresql默认为5432)/数据库'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")

