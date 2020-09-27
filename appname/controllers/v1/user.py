from flask import Blueprint, request

from appname.models import User, Role, Permission, RolePermission
from appname.errors import UsernameExists, DeleteFailed
from appname.utils.middleware import permission_require, not_allowed
from appname.extentions import db
from .base import BaseView, register_api


class UserView(BaseView):
    model = User
    method_decorators = {
        "get": permission_require("all_user", "get_user"),
        "post": permission_require("all_user", "create_user"),
        "patch": permission_require("all_user", "update_user"),
        "delete": permission_require("all_user", "delete_user")
    }
    create_required_fields = ['username', 'name', 'password']
    patch_allowed_fields = ['name', 'password']

    def filter_cursor(self, cursor):
        param = request.args

        if 'name' in param:
            cursor = cursor.filter_by(name=param['name'])

        return cursor

    def order_cursor(self, cursor):
        cursor = cursor.order_by(User.member_since.desc())

        return cursor

    def create_check(self, post_data):
        super().create_check(post_data),

        exist_username_user = User.query.filter_by(username=post_data['username']).first()
        if exist_username_user:
            raise UsernameExists


class RoleView(BaseView):
    model = Role
    method_decorators = {
        "get": permission_require("all_role", "get_role"),
        "post": permission_require("all_role", "create_role"),
        "patch": permission_require("all_role", "update_role"),
        "delete": permission_require("all_role", "delete_role")
    }

    create_required_fields = ['name', 'permission_ids']
    patch_allowed_fields = ['name', 'permission_ids']

    def create_obj(self, post_data):
        permission_ids = post_data.pop("permission_ids")

        obj = super().create_obj(post_data)

        for p_id in permission_ids:
            r_p = RolePermission(**{"role_id": obj.id, "permission_id": p_id})
            db.session.add(r_p)
        db.session.commit()

        return obj

    def patch_obj(self, obj, post_data):
        permission_ids = post_data.pop("permission_ids")

        obj = super().patch_obj(obj, post_data)

        RolePermission.query.filter_by(role_id=obj.id).delete()

        for p_id in permission_ids:
            r_p = RolePermission(**{"role_id": obj.id, "permission_id": p_id})
            db.session.add(r_p)

        db.session.commit()

        return obj

    def delete_check(self, obj):
        exists_users = User.query.filter_by(role_id=obj.id).all()
        if exists_users:
            raise DeleteFailed

    def delete_obj(self, obj):

        super().delete_obj(obj)

        RolePermission.query.filter_by(role_id=obj.id).delete()


class PermissionView(BaseView):
    model = Permission
    method_decorators = {
        "get": permission_require("all_permission"),
        "post": not_allowed(),
        "patch": not_allowed(),
        "delete": not_allowed()
    }


bp = Blueprint('user', __name__)

register_api(bp, UserView, 'user_api', '/users')
register_api(bp, RoleView, 'role_api', '/roles')
register_api(bp, PermissionView, 'permission_api', '/permissions')
