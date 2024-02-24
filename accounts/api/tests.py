from rest_framework.reverse import reverse

from tests.BaseTests import CustomAPITestCase
from .urls import app_name
from ..models import User


# Create your tests here.


class TestListUserApiView(CustomAPITestCase):

    def test_admin_get_list_users(self):
        """Тестирование того, что администратор получит список пользователей"""
        self.client.force_login(self.admin)
        response = self.client.get(reverse(f'{app_name}:api-list-users'))
        self.assertEqual(200, response.status_code)

    def test_user_get_list_users(self):
        """Тестирование того, что пользователь не получит список пользователей"""
        self.client.force_login(self.user)
        response = self.client.get(reverse(f'{app_name}:api-list-users'))
        self.assertEqual(403, response.status_code)

    def test_anonymous_get_list_users(self):
        """Тестирование того, что анонимный пользователь не получит список пользователей"""
        response = self.client.get(reverse(f'{app_name}:api-list-users'))
        self.assertEqual(403, response.status_code)

    def test_create_new_user(self):
        """Тестирование того, что будет создан новый пользователь"""
        user_for_create: dict = {
            'username': 'test_new_user',
            'email': 'roma.makhunov@gmail.com',
            'password': 'test_password_new_user'
        }
        response = self.client.post(reverse(f'{app_name}:api-list-users'), data=user_for_create)
        self.assertTrue(User.objects.filter(username=user_for_create.get('username')).exists())
        self.assertEqual(201, response.status_code)
