from flask_babel import lazy_gettext as _


class ApiError(Exception):
    code = 0
    msg = ''

    def __init__(self, msg=None, payload=None):
        Exception.__init__(self)
        if msg is not None:
            self.msg = msg
        self.payload = payload

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "payload": self.payload
        }


class BadRequest(ApiError):
    code = 1000
    msg = _("bad request")


class NotAllowed(ApiError):
    code = 1001
    msg = _("not allowed")


class PermissionDeny(ApiError):
    code = 1002
    msg = _("permission deny")


class UsernameOrPasswordWrong(ApiError):
    code = 1003
    msg = _("username or password wrong")


class UsernameExists(ApiError):
    code = 1004
    msg = _("username already exists")


class Unauthorized(ApiError):
    code = 1010
    msg = _("unauthorized")


class UnauthorizedTokenWrong(ApiError):
    code = 1011
    msg = _("unauthorized token wrong")


class UnauthorizedTokenExpire(ApiError):
    code = 1012
    msg = _("unauthorized token expire")


class UnauthorizedUserNotExist(ApiError):
    code = 1013
    msg = _("unauthorized user not exist")


class ResourceNotFound(ApiError):
    code = 4000
    msg = _("resource not found")


class DeleteFailed(ApiError):
    code = 4010
    msg = _("delete failed")
