from flask import Blueprint
from flask_jwt_extended import jwt_required, get_raw_jwt, get_jwt_identity, get_jwt_claims, current_user

from appname.utils.middleware import permission_require
from appname.utils.controller_utils import success_resp


@jwt_required
def test():
    print(get_raw_jwt())
    print(get_jwt_identity())
    print(get_jwt_claims())
    print(current_user)
    return success_resp({'ping': 'pang'})


bp = Blueprint('test', __name__)


bp.add_url_rule("/test", "test", test, methods=["GET"])

