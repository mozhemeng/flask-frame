from flask import request
from flask.views import MethodView

from appname.utils.controller_utils import success_resp, page_cursor
from appname.errors import BadRequest, ResourceNotFound
from appname.extentions import db


class BaseView(MethodView):

    model = db.Model
    method_decorators = []

    create_required_fields = []
    patch_allowed_fields = []

    def dispatch_request(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method

        if isinstance(self.method_decorators, dict):
            decorators = self.method_decorators.get(request.method.lower(), [])
        else:
            decorators = self.method_decorators

        if not isinstance(decorators, list):
            decorators = [decorators]

        for decorator in decorators:
            meth = decorator(meth)

        resp = meth(*args, **kwargs)

        return resp

    def filter_cursor(self, cursor):
        return cursor

    def order_cursor(self, cursor):
        return cursor

    def get_obj_by_pk(self, pk):
        obj = self.model.query.get(pk)
        if not obj:
            raise ResourceNotFound
        return obj

    def get_one(self, pk):
        obj = self.get_obj_by_pk(pk)
        return success_resp(obj.to_dict())

    def structure_list(self, objs):
        return [obj.to_dict() for obj in objs]

    def get_list(self):
        cursor = self.model.query
        cursor = self.filter_cursor(cursor)
        cursor = self.order_cursor(cursor)
        cursor, page_resp = page_cursor(cursor)
        objs = cursor.all()
        res = self.structure_list(objs)

        return success_resp(res, **page_resp)

    def get(self, pk=None):
        if pk is None:
            return self.get_list()
        else:
            return self.get_one(pk=pk)

    def get_post_data(self):
        return request.json

    def create_check(self, post_data):
        if self.create_required_fields:
            for key in self.create_required_fields:
                if key not in post_data:
                    raise BadRequest(f"need {key} to create")

    def before_create(self, post_data):
        return post_data

    def create_obj(self, post_data):
        obj = self.model(**post_data)
        obj.save()
        return obj

    def after_create(self, obj):
        return obj.to_dict()

    def post(self):
        post_data = self.get_post_data()

        self.create_check(post_data)
        post_data = self.before_create(post_data)

        obj = self.create_obj(post_data)

        resp = self.after_create(obj)

        return success_resp(resp)

    def patch_check(self, obj,  post_data):
        if self.patch_allowed_fields:
            for key in post_data:
                if key not in self.patch_allowed_fields:
                    raise BadRequest(f"{key} can not be patched")

    def before_patch(self, obj, post_data):
        return post_data

    def patch_obj(self, obj, post_data):
        for k, v in post_data.items():
            setattr(obj, k, v)
        obj.save()
        return obj

    def after_patch(self, obj):
        return obj.to_dict()

    def patch(self, pk):
        post_data = self.get_post_data()
        obj = self.get_obj_by_pk(pk)

        self.patch_check(obj, post_data)
        post_data = self.before_patch(obj, post_data)

        obj = self.patch_obj(obj, post_data)

        resp = self.after_patch(obj)

        return success_resp(resp)

    def delete_check(self, obj):
        pass

    def delete_obj(self, obj):
        obj.delete()

    def delete(self, pk):
        obj = self.get_obj_by_pk(pk)

        self.delete_check(obj)

        self.delete_obj(obj)

        return success_resp()


def register_api(app, view, endpoint, url, pk='pk', pk_type='int'):
    view_func = view.as_view(endpoint)
    url = url.rstrip('/')
    app.add_url_rule(f'{url}', view_func=view_func, methods=["GET", "POST"])
    app.add_url_rule(f'{url}/<{pk_type}:{pk}>', view_func=view_func, methods=["GET", "PATCH", "DELETE"])

