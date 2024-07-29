from django.test import TestCase, Client
from django.urls import reverse
from faker import Faker
from http import HTTPStatus
from django.contrib.auth.models import User


class UsersTest(TestCase):
    def test_users_list(self):
        client = Client()
        response = client.get(reverse('users_index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('users', response.context)


class UsersCreateTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_create_get(self):
        response = self.client.get(reverse('users_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_create_post(self):
        faker = Faker()
        username = faker.user_name()
        password = faker.password(length=10)
        self.client.post(reverse('users_create'),
                         data={'username': username,
                               'password1': password,
                               'password2': password})
        user = User.objects.last()
        self.assertEqual(user.username, username)
        user.delete()


class UserUpdateTest(TestCase):
    def setUp(self):
        self.client = Client()
        faker = Faker()

        username_1 = faker.user_name()
        password_1 = faker.password(length=10)
        username_2 = faker.user_name()
        password_2 = faker.password(length=10)
        self.authorized_user = User.objects.create_user(username=username_1,
                                                        password=password_1)
        self.unauthorized_user = User.objects.create_user(username=username_2,
                                                          password=password_2)
        self.authorized_user.save()
        self.unauthorized_user.save()

        self.client.force_login(self.authorized_user)

        self.new_username = faker.user_name()
        self.new_user_data = {'username': self.new_username}

    def tearDown(self):
        self.authorized_user.delete()
        self.unauthorized_user.delete()

    def test(self):
        self._test_update_user_allowed_get()
        self._test_update_user_restricted_get()
        self._test_update_user_allowed_post()
        self._test_update_user_restricted_post()

    def _test_update_user_allowed_get(self):
        response = self.client.get(
            reverse('user_update', kwargs={'id': self.authorized_user.id})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def _test_update_user_restricted_get(self):
        response = self.client.get(
            reverse('user_update', kwargs={'id': self.unauthorized_user.id})
        )

        self.assertFalse(response.status_code == HTTPStatus.OK)

    def _test_update_user_allowed_post(self):
        response = self.client.post(
            reverse('user_update', kwargs={'id': self.authorized_user.id}),
            data=self.new_user_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(self.authorized_user.username, self.new_username)

    def _test_update_user_restricted_post(self):
        response = self.client.post(
            reverse('user_update', kwargs={'id': self.unauthorized_user.id}),
            data=self.new_user_data
        )
        self.assertFalse(response.status_code == HTTPStatus.FOUND)
        self.assertFalse(self.authorized_user.username == self.new_username)
