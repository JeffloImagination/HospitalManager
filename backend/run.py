from app.__init__ import create_app
from app.utils import test_database_connection, load_initial_data
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = create_app()
db = SQLAlchemy(app)

if __name__ == "__main__":
    # 加载初始数据
    # with app.app_context():
    #     load_initial_data()

    app.run(debug=True)
    # test_database_connection()
