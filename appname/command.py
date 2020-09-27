import os
import click

from flask.cli import AppGroup


babel_cli = AppGroup('babel')
deploy_cli = AppGroup('deploy')


@babel_cli.command()
@click.option('--lang', default="zh", help='language code just like "zh","jp"')
def init(lang):
    """create .pot and translations files with --lang option to specified language"""
    os.system(
        'pybabel extract -F ./babel/babel.cfg -k lazy_gettext -o ./babel/messages.pot appname'
    )
    os.system(
        'pybabel init -i ./babel/messages.pot -d appname/translations -l {}'.format(lang)
    )


@babel_cli.command()
def update():
    """update .pot and translations files"""
    os.system(
        'pybabel extract -F ./babel/babel.cfg -k lazy_gettext -o ./babel/messages.pot appname')
    os.system(
        'pybabel update -i ./babel/messages.pot -d appname/translations'
    )


@babel_cli.command()
def compile():
    """complete the translation process"""
    os.system('pybabel compile -d appname/translations')


@deploy_cli.command()
def init():
    print("start to deploy now")
    from appname.models import User, Permission
    print("insert permission")
    Permission.insert_permissions()
    print("insert admin user")
    User.insert_admin()


@deploy_cli.command(name='permission')
def insert_permission():
    from appname.models import Permission
    print("insert permission")
    Permission.insert_permissions()
