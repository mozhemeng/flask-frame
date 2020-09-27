from flask import Flask

from appname.controllers import controller_mapping
from appname.errors import error_handler_mapping
from appname.utils.custom import CustomJSONEncoder
from appname.utils.babel_utils import get_locale
from appname.extentions import babel, db, migrate, redis_store, jwt, mongodb, data_mongodb
from appname.command import babel_cli, deploy_cli


def create_app(config_name):
    # app创建
    app = Flask(__name__)
    # 配置导入
    app.config.from_object(config_name)

    # 蓝图注册
    for controller_version, bp_list in controller_mapping.items():
        for bp, prefix in bp_list:
            if prefix:
                url_prefix = f'/api/{controller_version}/{prefix}'
            else:
                url_prefix = f'/api/{controller_version}'
            app.register_blueprint(bp, url_prefix=url_prefix)

    # 插件注册
    babel.init_app(app)
    babel.localeselector(get_locale)
    db.init_app(app)
    db.app = app
    migrate.init_app(app, db=db)
    redis_store.init_app(app)
    jwt.init_app(app)
    mongodb.init_app(app)

    # 错误处理
    for err, handle in error_handler_mapping:
        app.register_error_handler(err, handle)

    # 添加命令
    app.cli.add_command(babel_cli)
    app.cli.add_command(deploy_cli)

    # 定制
    app.json_encoder = CustomJSONEncoder

    return app
