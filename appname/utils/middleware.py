from functools import wraps

from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from flask import current_app

from appname.errors import PermissionDeny, NotAllowed


def permission_require(*need_permissions):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            if get_jwt_claims().get("username") == current_app.config["SUPER_ADMIN_USERNAME"]:
                return func(*args, **kwargs)

            has_permissions = get_jwt_claims().get("permissions", [])
            if set(need_permissions) & set(has_permissions):
                return func(*args, **kwargs)

            raise PermissionDeny

        return wrapper
    return decorator


def not_allowed():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            raise NotAllowed
        return wrapper
    return decorator
