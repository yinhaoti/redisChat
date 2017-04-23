import hashlib
import os

from . import ModelMixin
from . import db


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(), unique=True)
    password = db.Column(db.Text)

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def valid_username(cls, username):
        return User.query.filter_by(username=cls.username).first() == None

    @classmethod
    def update(cls, id, form):
        m = cls.query.get(id)
        m.username = form.get('username', m.username)
        m.password = form.get('password', m.password)
        m.save()

    # 验证注册用户的合法性
    def valid(self):
        valid_username = self.valid_username()
        valid_username_len = len(self.username) >= 6
        valid_password_len = len(self.password) >= 6
        msgs = []
        if not valid_username:
            message = '用户名已经存在'
            msgs.append(message)
        if not valid_username_len:
            message = '用户名长度必须大于等于 6'
            msgs.append(message)
        if not valid_password_len:
            message = '密码长度必须大于等于 6'
            msgs.append(message)
        status = valid_username and valid_username_len and valid_password_len
        return status, msgs
