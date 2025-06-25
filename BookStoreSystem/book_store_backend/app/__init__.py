from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
# 修改为相对导入
from .config import config_map

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

def create_app(config_name='default'):
    """工厂函数，创建Flask应用实例"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config_map[config_name])
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    
    # 导入并注册蓝图
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 导入错误处理
    from .errors import register_error_handlers
    register_error_handlers(app)
    
    # 导入命令行命令
    from .commands import register_commands
    register_commands(app)
    
    return app