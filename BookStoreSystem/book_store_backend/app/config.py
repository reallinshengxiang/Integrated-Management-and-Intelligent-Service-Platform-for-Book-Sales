# book_store_backend/app/config.py
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 应用配置
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # 数据库配置
    
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
    )
    SQLALCHEMY_DATABASE_URI = 'postgresql://linshengxiang:Password!2025@localhost:5433/bookstoredb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1小时
    GITHUB_TOKEN = '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'
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    # 其他配置
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
        
class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # 使用内存数据库进行测试
    JWT_ACCESS_TOKEN_EXPIRES = 300  # 5分钟

# 配置映射
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}