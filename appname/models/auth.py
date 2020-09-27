import time
import hashlib
import json

from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

from appname.extentions import db
from .base import BaseModel
from appname.utils.path_utils import DEPLOY_DIR


class Permission(BaseModel):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256), comment="描述")

    @staticmethod
    def insert_permissions():
        with open(DEPLOY_DIR.joinpath("permissions.json")) as f:
            permissions = json.load(f)
        for permission in permissions:
            exists = Permission.query.filter_by(name=permission['name']).first()
            if exists:
                continue
            obj = Permission(**permission)
            db.session.add(obj)
        db.session.commit()


class Role(BaseModel):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256), comment="描述")

    @property
    def permissions(self):
        relates = RolePermission.query.filter_by(role_id=self.id).all()
        p_ids = [relate.permission_id for relate in relates]
        if not p_ids:
            return []
        return Permission.query.filter(Permission.id.in_(p_ids)).all()

    def to_dict(self):
        res = super().to_dict()
        res['permissions'] = [{
            "id": p.id,
            "name": p.name
        } for p in self.permissions]

        return res


class RolePermission(BaseModel):
    __tabelname__ = 'roles_permissions'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, nullable=False)
    permission_id = db.Column(db.Integer, nullable=False)


class User(BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    member_since = db.Column(db.BigInteger, default=time.time, comment="注册时间")
    last_seen = db.Column(db.BigInteger, default=time.time, comment="最近登陆时间")
    role_id = db.Column(db.Integer)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def role(self):
        if self.role_id is None:
            return
        return Role.query.get(self.role_id)

    @property
    def role_name(self):
        role = self.role
        if role:
            return role.name

    @property
    def permission_names(self):
        role = self.role
        if role is None:
            return []
        return [p.name for p in role.permissions]

    def ping(self):
        self.last_seen = time.time()
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @staticmethod
    def insert_admin():
        exists = User.query.filter_by(username=current_app.config["SUPER_ADMIN_USERNAME"]).first()
        if exists:
            print(f"super admin already exists")
            return
        md5 = hashlib.md5()
        md5.update(current_app.config["SUPER_ADMIN_PW"].encode('utf-8'))
        admin_password = md5.hexdigest()
        admin_info = {
            "username": "_superadmin",
            "name": "超级管理员",
            "password": admin_password
        }
        admin = User(**admin_info)
        db.session.add(admin)
        db.session.commit()

    def to_dict(self):
        res = super().to_dict()

        res['role'] = self.role_name

        return res
