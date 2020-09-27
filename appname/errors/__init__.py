from werkzeug.exceptions import InternalServerError

from .error_handler import handle_api_error, handle_internal_error
from .error_instance import *


error_handler_mapping = [
    (ApiError, handle_api_error),
    (InternalServerError, handle_internal_error)
]