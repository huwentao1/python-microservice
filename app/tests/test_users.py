import json
from app.tests.base import BaseTestCase


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

