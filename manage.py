import unittest
from flask_script import Manager
from app.api.models import User
from app import create_app, db

app = create_app()

manage = Manager(app)
import coverage

COV = coverage.coverage(branch=True, include="app/*", omit=["app/tests/*"])

COV.start()


@manage.command
def cov():
    """执行代码覆盖组件"""
    tests = unittest.TestLoader().discover(start_dir="app/tests", pattern="test_*.py")

    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("代码覆盖结果为: ")
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manage.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@manage.command
def test():
    """运行测试"""
    tests = unittest.TestLoader().discover(start_dir="app/tests", pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manage.command
def seed_db():
    """Seeds th database"""
    db.session.add(User(username="hwt1", email="hwt1@163.com"))
    db.session.add(User(username="hwt2", email="hwt2@163.com"))
    db.session.commit()


if __name__ == "__main__":
    manage.run()
