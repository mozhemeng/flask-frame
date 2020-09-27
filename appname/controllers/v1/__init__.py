from appname.controllers.v1.auth import bp as auth_bp
from appname.controllers.v1.test import bp as test_bp
from appname.controllers.v1.user import bp as user_bp


bp_list = [(auth_bp, 'auth'), (test_bp, 'test'), (user_bp, '')]


__all__ = ['bp_list']
