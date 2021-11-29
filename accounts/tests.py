from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class AccountTestCase(APITestCase):
    def setUp(self):
      self.host = 'http://127.0.0.1:8000'

    def test_create_account(self):
        response = self.client.post(
              f'{self.host}/accounts/',
              data={"username": "example", "password": "example", "email": "example@gmail.com"},
        )

        user = User.objects.filter(username='example')
        self.assertTrue(user.exists())
        self.assertEqual(response.status_code, 201)