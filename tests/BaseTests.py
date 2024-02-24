from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase

from accounts.models import User
from tests.fakeData import TestDataUsers


class CustomAPITestCase(APITestCase):
    admin: User = None
    user: User = None

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        dict_admin = {
            'username': 'AdminTestListUserApiView',
            'email': 'AdminTest@gmail.com',
            'password': f'{make_password('AdminTestListUserApiView')}'}
        dict_user = {
            'username': 'UserTestListUserApiView',
            'email': 'UserTest@gmail.com',
            'password': f'{make_password('UserTestListUserApiView')}'
        }
        cls.admin = User.objects.create_superuser(**dict_admin)
        cls.user = User.objects.create_user(**dict_user)
        User.objects.bulk_create(TestDataUsers.get_list_fake_users())


