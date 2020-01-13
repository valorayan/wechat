# coding:utf-8
import logging
import redis
from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from logging.handlers import RotatingFileHandler

# 数据库
db = SQLAlchemy()

# 创建redis连接对象
redis_store = None

# 日志信息
logging.basicConfig(level=logging.DEBUG)  # 设置日志的记录等级
# 创建日志记录器，指明日志的保存路径，每个日志的文件大小，保存的日志文件数量
file_log_handler = RotatingFileHandler('logs/log', maxBytes=1024 * 1024 * 100, backupCount=10)
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s：%(lineno)d -  %(message)s"  # 日志格式化输出
# 创建日志记录的格式
formatter = logging.Formatter(LOG_FORMAT)
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)


# 工厂模式
def create_app(config_name):
    """
    创建flask的应用对象
    :param config_name: str 配置模式的名字（"develop","product"）
    :return:
    """
    app = Flask(__name__)
    # 根据配置模式的名字 获取对应的配置参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)
    # 使用app初始化数据库
    db.init_app(app)
    # 初始化redis
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # 利用flask-session, 将session数据保存到redis中
    Session(app)

    # 为flask 补充 csrf防护
    # CSRFProtect(app)

    # 注册蓝图
    from project import api_v1
    app.register_blueprint(api_v1.api, url_prefix='/api/v1')

    return app
