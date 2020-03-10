import unittest
from flask_script import Manager
from app import create_app, db

app = create_app()

manage = Manager(app)


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


if __name__ == "__main__":
    manage.run()
