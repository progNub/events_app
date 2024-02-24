from django.contrib.auth.hashers import make_password
from faker import Faker

from accounts.models import User

fake = Faker('ru-RU')


class TestDataUsers:
    @staticmethod
    def get_list_fake_users(limit=5):
        users: [User] = []
        for i in range(limit):
            user = User()
            user.username = fake.unique.user_name()
            user.first_name = fake.first_name()
            user.last_name = fake.last_name()
            user.email = fake.email()
            user.is_superuser = False
            user.is_staff = False
            user.password = make_password(fake.password())
            users.append(user)
        return users
