from backend import create_app
from flask_migrate import upgrade
import MySQLdb
from flask import request, Blueprint, jsonify
from models import db, Product  # 导入模型

app = create_app()


def create_database_if_not_exists():
    """测试数据库是否存在，不存在则创建"""
    connection = MySQLdb.connect(
        user='root',
        password='000150',  # replace with your password
        host='localhost'
    )
    cursor = connection.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS xd_go;')
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    # Ensure the database exists
    create_database_if_not_exists()

    # Run database migrations to create tables
    with app.app_context():
        upgrade()  # This will apply migrations and create tables

    app.run(port=5001, debug=True)

