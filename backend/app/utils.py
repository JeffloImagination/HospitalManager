'''
工具文具文件
'''
from .database import execute_sql_script
from sqlalchemy import create_engine

def load_initial_data():
    """加载初始化数据"""
    # execute_sql_script("sql_scripts/create_tables.sql")
    execute_sql_script("sql_scripts/insert_departments.sql")
    execute_sql_script("sql_scripts/insert_doctors.sql")
    execute_sql_script("sql_scripts/insert_patients.sql")
    execute_sql_script("sql_scripts/insert_registrations.sql")

# 测试数据库连接函数
def test_database_connection():
    database_url = "postgresql://hospital_admin:1234@localhost:5432/hospital_db"
    engine = create_engine(database_url)

    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")