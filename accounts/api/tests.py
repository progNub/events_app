from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import User


# Create your tests here.


class TestListUserApiView(APITestCase):
    admin: User = None
    user: User = None

    @classmethod
    def setUpTestData(cls):
        admin = {
            'username': 'AdminTestListUserApiView',
            'email': 'AdminTest@gmail.com',
            'password': 'AdminTestListUserApiView'}
        user = {
            'username': 'UserTestListUserApiView',
            'email': 'UserTest@gmail.com',
            'password': 'UserTestListUserApiView'
        }
        cls.admin = User.objects.create_superuser(admin)
        cls.user = User.objects.create_user(user)

    def test_admin_get_list_users(self):
        """Тестирование того, что администратор получит список пользователей"""
        self.client.force_login(self.admin)
        response = self.client.get(reverse('api:api-list-users'))
        self.assertEqual(200, response.status_code)

    def test_user_get_list_users(self):
        """Тестирование того, что пользователь не получит список пользователей"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('api:api-list-users'))
        self.assertEqual(403, response.status_code)

    def test_anonymous_get_list_users(self):
        """Тестирование того, что анонимный пользователь не получит список пользователей"""
        response = self.client.get(reverse('api:api-list-users'))
        self.assertEqual(403, response.status_code)

    def test_create_new_user(self):
        """Тестирование того, что анонимный пользователь не получит список пользователей"""
        user_for_create: dict = {
            'username': 'test_new_user',
            'email': 'roma.makhunov@gmail.com',
            'password': 'test_password_new_user'
        }
        response = self.client.post(reverse('api:api-list-users'), data=user_for_create)
        self.assertEqual(201, response.status_code)
