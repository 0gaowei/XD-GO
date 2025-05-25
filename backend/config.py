import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # 设置数据库连接
    SECRET_KEY = os.environ.get('SECRET_KEY')  # 用于 JWT 加密
    CORS_HEADERS = 'Content-Type'  # 用于跨域设置


class DevelopmentConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:003620@localhost:3306/xd_go'

    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG = False
