import math

from flask import jsonify, request, current_app


def success_resp(res=None, **kwargs):
    if res is None:
        res = []
    resp = {'code': 0,
            'msg': 'success',
            'results': res}
    kwargs.pop('code', None)
    kwargs.pop('msg', None)
    kwargs.pop('results', None)
    resp.update(kwargs)
    return jsonify(resp)


def parse_page():
    args = request.args
    paged = int(args.get('paged', 1))
    page = int(args.get('page', 1))
    page_size = int(args.get('page_size', 10))

    if page_size > current_app.config["MAX_PAGE_SIZE"]:
        page_size = current_app.config["MAX_PAGE_SIZE"]

    return {'paged': paged, 'page': page, 'page_size': page_size}


def page_cursor(cursor):
    page_resp = {}

    page_info = parse_page()

    total_count = cursor.count()
    if page_info['paged'] or total_count > current_app.config["MAX_PAGE_SIZE"]:
        total_page = math.ceil(total_count / page_info['page_size'])
        page = page_info['page']
        if page > total_page:
            page = total_page
        skip = (page - 1) * page_info['page_size']
        cursor = cursor.offset(skip).limit(page_info['page_size'])
        page_resp = {'total_count': total_count, 'total_page': total_page, 'now_page': page}

    return cursor, page_resp
