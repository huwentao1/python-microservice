import os


class BasicConfig:
    """基础的配置信息"""

    DEBUG = False
    TESTING = False
    SECRET_KEY = "secret"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BasicConfig):
    """测试环境配置"""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")


class DevelopmentConfig(BasicConfig):
    """开发环境"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_DEV_URL")


class ProjectConfig(BasicConfig):
    """生产环境"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_PROJECT_URL")
