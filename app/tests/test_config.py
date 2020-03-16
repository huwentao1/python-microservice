from flask import current_app
from flask_testing import TestCase
from app import create_app
app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object("app.config.DevelopmentConfig")
        return app

    def test_app_is_development(self):
        """确保开发环境的正确"""
        self.assertTrue(app.config["SECRET_KEY"] == "secret")
        self.assertTrue(app.config["DEBUG"] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config["SQLALCHEMY_DATABASE_URI"]
            == "mysql+pymysql://root:123456@192.168.50.78:3306/users_dev"
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object("app.config.TestingConfig")
        return app

    def test_app_is_test(self):
        self.assertTrue(app.config["SECRET_KEY"] == "secret")
        self.assertTrue(app.config["DEBUG"])
        self.assertTrue(app.config["TESTING"])
        self.assertTrue(
            app.config["SQLALCHEMY_DATABASE_URI"]
            == "mysql+pymysql://root:123456@192.168.50.78:3306/users_test"
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object("app.config.ProjectConfig")
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config["SECRET_KEY"] == "secret")
        self.assertFalse(app.config["DEBUG"])
        self.assertFalse(app.config["TESTING"])
