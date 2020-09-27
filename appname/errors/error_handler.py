from flask import jsonify


def handle_api_error(error):
    return jsonify(error.to_dict())


def handle_internal_error(error):
    print("================")
    print("================")
    return error
