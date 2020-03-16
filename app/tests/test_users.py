import json
import time
from app.tests.base import BaseTestCase

from app.api.models import User
from app import db


class TestUserService(BaseTestCase):
    def test_users(self):
        """确保ping服务是正常的"""
        response = self.client.get("/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user(self):
        """确保能够正确添加一个用户到数据库中"""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({"username": "hwt", "email": "hwt@163.com"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("hwt@163.com was add.", data["message"])
            self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self):
        """如果json对象为空，抛出一个错误"""
        with self.client:
            response = self.client.post(
                "/users", data=json.dumps({}), content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("data is not null.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_invalid_json_keys(self):
        """如果email或者username为空，抛出一个错误"""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({"username": "hwt"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Email can not null.", data["message"])
            self.assertIn("fail", data["status"])
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({"email": "hwt@163.com"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Username can not null.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_same_user(self):
        """如果添加了相同的用户名，抛出一个错误"""
        with self.client:
            self.client.post(
                "/users",
                data=json.dumps({"username": "hwt", "email": "hwt@163.com"}),
                content_type="application/json",
            )
            response = self.client.post(
                "/users",
                data=json.dumps({"username": "hwt", "email": "hwt@163.com"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Sorry. That email already exists.", data["message"])
            self.assertIn("fail", data["status"])

    def test_get_user(self):
        """确保可以查询到一个用户"""
        user = User(username="hwt", email="hwt@163.com")
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.get(
                "/users/%s" % user.id, content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode())
            self.assertIn("success", data["status"])
            self.assertIn(user.username, data["message"]["username"])
            self.assertIn(user.email, data["message"]["email"])

    def test_get_user_no_id(self):
        """确保id不存在时爆出一个错误"""
        with self.client:
            response = self.client.get("/users/xxx")
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data.decode())
            self.assertIn("fail", data["status"])
            self.assertIn("xxx id not exists.", data["message"])

    def test_get_users(self):
        """确保可以获取一个用户列表"""
        user1 = User(username="hwt1", email="hwt1@163.com")
        user2 = User(username="hwt2", email="hwt2@163.com")
        db.session.add(user1)
        db.session.add(user2)
        with self.client:
            response = self.client.get("/users")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode())
            self.assertIn("success", data["status"])
            self.assertEqual(
                time.mktime(user1.created_at.timetuple()),
                data["user"][0].get("created_at"),
            )
            self.assertEqual(user1.username, data["user"][0].get("username"))
            self.assertEqual(user1.email, data["user"][0].get("email"))
            self.assertEqual(user1.id, data["user"][0].get("id"))

            self.assertEqual(
                time.mktime(user2.created_at.timetuple()),
                data["user"][1].get("created_at"),
            )
            self.assertEqual(user2.username, data["user"][1].get("username"))
            self.assertEqual(user2.email, data["user"][1].get("email"))
            self.assertEqual(user2.id, data["user"][1].get("id"))
