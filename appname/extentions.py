from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager


babel = Babel()
db = SQLAlchemy()
migrate = Migrate()
redis_store = FlaskRedis()
jwt = JWTManager()
mongodb = PyMongo()
data_mongodb = PyMongo()
