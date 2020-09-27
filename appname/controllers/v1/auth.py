from flask import request, Blueprint, current_app
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jti,
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, jwt_required)

from appname.models import User
from appname.errors import (UsernameOrPasswordWrong, UnauthorizedUserNotExist, Unauthorized,
                            UnauthorizedTokenExpire, UnauthorizedTokenWrong, handle_api_error)
from appname.utils.controller_utils import success_resp
from appname.utils.auth_utils import merge_jit_key, revoke_all_key
from appname.extentions import redis_store, jwt


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    identity = decrypted_token['identity']
    key = merge_jit_key(identity, jti)
    entry = redis_store.get(key)
    if entry is None:
        return True
    return entry == 'true'


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.query.get(identity)
    if not user:
        return
    return {
        "username": user.username,
        "name": user.name,
        "role": user.role_name,
        "permissions": user.permission_names
    }


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    # 注意：每次请求都从数据库加载用户，会使性能降低
    return User.query.get(identity)


@jwt.user_loader_error_loader
def user_loader_error_loader_callback():
    return handle_api_error(UnauthorizedUserNotExist())


@jwt.unauthorized_loader
def unauthorized_loader_callback(s):
    return handle_api_error(Unauthorized())


@jwt.expired_token_loader
def expired_token_loader_callback(s):
    return handle_api_error(UnauthorizedTokenExpire())


@jwt.invalid_token_loader
def invalid_token_loader_callback(s):
    return handle_api_error(UnauthorizedTokenWrong())


@jwt.revoked_token_loader
def revoked_token_loader_callback():
    return handle_api_error(UnauthorizedTokenWrong())


def login():
    data = request.json
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if not user:
        raise UsernameOrPasswordWrong
    if not user.verify_password(password):
        raise UsernameOrPasswordWrong
    user.ping()

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    access_jti = get_jti(encoded_token=access_token)
    refresh_jti = get_jti(encoded_token=refresh_token)
    access_key = merge_jit_key(user.id, access_jti)
    refresh_key = merge_jit_key(user.id, refresh_jti)
    redis_store.set(access_key, 'false',  current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] * 1.1)
    redis_store.set(refresh_key, 'false', current_app.config['JWT_REFRESH_TOKEN_EXPIRES'] * 1.1)

    res = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

    return success_resp(res)


@jwt_refresh_token_required
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    access_jti = get_jti(encoded_token=access_token)
    access_key = merge_jit_key(identity, access_jti)
    redis_store.set(access_key, 'false', current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] * 1.1)

    res = {
        "access_token": access_token
    }

    return success_resp(res)


@ jwt_required
def logout():
    identity = get_jwt_identity()
    revoke_all_key(identity)
    return success_resp()


bp = Blueprint('auth', __name__)


bp.add_url_rule("/login", "login", login, methods=["POST"])
bp.add_url_rule("/refresh", "refresh", refresh, methods=["POST"])
bp.add_url_rule("/logout", "logout", logout, methods=["DELETE"])
