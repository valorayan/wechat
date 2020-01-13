# coding:utf-8
from project import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # 生成hash密码， 校验hash密码


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now)


class User(BaseModel, db.Model):
    """用户模型"""

    __table_name = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    houses = db.relationship("House", backref="user")  # 用户发布的房屋

    @property
    def password(self):
        """获取password属性时被调用"""
        raise AttributeError("不可读")

    @password.setter
    def password(self, passwd):
        """设置password属性时被调用，设置密码加密"""
        self.password_hash = generate_password_hash(passwd)

    def check_password(self, passwd):
        """校验密码正确性"""
        return check_password_hash(self.password_hash, passwd)

    def to_dict(self):
        """将对象设置为字典"""
        user_dict = {
            "user_id": self.id,
            "user_name":self.name,
            "create_time":self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return user_dict
