import os
import datetime
import time
from decimal import Decimal

from flask import Flask
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, Decimal):
                return float(obj)

            if isinstance(obj, datetime.datetime):
                return time.mktime(obj.timetuple())

            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def create_app():
    app = Flask(__name__)
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)
    # 安装扩展
    app.json_encoder = CustomJSONEncoder
    db.init_app(app)
    # 注册blueprint
    from app.api.views import users_blueprint

    app.register_blueprint(users_blueprint)
    return app
