import datetime

from appname.extentions import db


def app_context_task(task_fun, *args, **kwargs):
    with db.app.app_context():
        task_fun(*args, **kwargs)


def test_job(string):
    print(datetime.datetime.now())
    print(f"this is test job: {string}")


def test_task(*args, **kwargs):
    app_context_task(test_job, *args, **kwargs)

