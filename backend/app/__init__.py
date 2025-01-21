from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config  # 根据需要引入配置
from .database import init_app
from .utils import load_initial_data
import click
# 注册蓝图（路由模块化处理时用）
from .routes import api
db = SQLAlchemy()

def create_app():
    """创建并初始化 Flask 应用"""
    app = Flask(__name__)
    CORS(app) # 启用 CORS，允许所有来源的跨域请求
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hospital_admin:1234@localhost:5432/hospital_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化扩展
    init_app(app)

    # 加载初始数据
    # load_initial_data()

    # @app.cli.command("load-initial-data")
    # def load_initial_data_command():
    #     """加载初始数据到数据库"""
    #     load_initial_data()
    
    app.register_blueprint(api, url_prefix='/api')

    return app
