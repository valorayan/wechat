# conding:utf-8
import redis


class Config(object):
    """配置信息"""

    SECRET_KEY = "Q3IJJOJIOJJOJouiououoiojoiJJOJOIOjoij&*THUH"
    # 数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:xg9270XGT@127.0.0.1:3306/test?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    # flask-session配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对session 的cookie隐藏
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 7  # session的有效期


class DevelopmentConfig(Config):
    """开发模式环境"""
    DEBUG = True


class ProductionConfig(Config):
    """生产模式环境"""
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig,
}
