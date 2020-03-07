class BasicConfig:
    """基础的配置信息"""

    DEBUG = False
    TESTING = False


class TestingConfig(BasicConfig):
    """测试环境配置"""

    DEBUG = True
    TESTING = True


class DevelopmentConfig(BasicConfig):
    """开发环境"""

    DEBUG = True


class ProjectConfig(BasicConfig):
    """生产环境"""

    pass
