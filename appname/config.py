import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


base_dir = os.getcwd()


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Shanghai')
    SUPER_ADMIN_USERNAME = "_superadmin"
    SUPER_ADMIN_PW = os.getenv("SUPER_ADMIN_PW", "123456")

    # controller
    MAX_PAGE_SIZE = os.getenv("MAX_PAGE_SIZE", 100)

    # sql
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # babel
    BABEL_DEFAULT_LOCALE = os.getenv('BABEL_DEFAULT_LOCALE', 'en')

    # redis
    REDIS_URL = os.getenv('REDIS_URL')

    # jwt
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_BLACKLIST_ENABLED = True

    # mongodb
    MONGO_URI = os.getenv('MONGO_URI')

    # aes
    AES_KEY = os.getenv('AES_KEY')

    # email
    EMAIL_SERVER = os.getenv('EMAIL_SERVER')
    SENDER_USER = os.getenv('SENDER_USER')
    SENDER_TOKEN = os.getenv('SENDER_TOKEN')
    SENDER_NAME = os.getenv('SENDER_NAME', 'flask-frame')
