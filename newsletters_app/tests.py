from rest_framework.test import APITestCase
from newsletters_app.models import Newsletter
from django.contrib.auth.models import User
from tags.models import Tag

class NewsletterTestCase(APITestCase):

    def setUp(self):
        self.host = 'http://127.0.0.1:8000'
        self.user = User.objects.create_user(username='user', email='user@gmail.com', password='12345')
        response = self.client.post(f'{self.host}/api/token/', {'username': 'user', 'password': '12345'} )
        self.user_token = response.data['access']

        self.admin = User.objects.create_superuser(username='admin', email='admin@gmail.com', password='admin')
        response = self.client.post(f'{self.host}/api/token/', {'username': 'admin', 'password': 'admin'} )
        self.admin_token = response.data['access']
        
        Tag.objects.create(name='food', slug='')

    def test_create_newsletter(self):
        response = self.client.post(
              f'{self.host}/newsletters/',
              data={"name": "test1", "description": "this is a test1", "tags": [1], "target": 200, "frequency": 14},
              HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )
        newsletter = Newsletter.objects.filter(name='test1')
        self.assertTrue(newsletter.exists())
        self.assertEqual(response.status_code, 201)

    def test_vote_newsletter(self):
        self.client.post(
              f'{self.host}/newsletters/',
              data={"name": "test2", "description": "this is a test2", "tags": [1], "target": 1, "frequency": 28},
              HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )
        response = self.client.patch(
              f'{self.host}/newsletters/1/vote/',
              HTTP_AUTHORIZATION=f'Bearer {self.user_token}'
        )
        
        self.assertEqual(len(Newsletter.objects.get(id=1).votes.all()), 1)
        self.assertTrue(Newsletter.objects.get(id=1).is_published)
        self.assertEqual(response.status_code, 201)

    def test_subscribe_newsletter(self):
        self.client.post(
              f'{self.host}/newsletters/',
              data={"name": "test2", "description": "this is a test2", "tags": [1], "target": 1, "frequency": 28},
              HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )
        newsletter = Newsletter.objects.get(id=1)
        newsletter.is_published = True
        newsletter.save()
        response = self.client.post(
            f'{self.host}/newsletters/1/subscribe/',
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'
        )
        
        self.assertEqual(len(newsletter.subs.all()), 1)
        self.assertEqual(response.status_code, 201)
    
    def test_unsubscribe_newsletter(self):
        self.client.post(
              f'{self.host}/newsletters/',
              data={"name": "test2", "description": "this is a test2", "tags": [1], "target": 1, "frequency": 28},
              HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )
        newsletter = Newsletter.objects.get(id=1)
        newsletter.is_published = True
        newsletter.save()
        response = self.client.post(
            f'{self.host}/newsletters/1/subscribe/',
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'
        )
        response = self.client.post(
            f'{self.host}/newsletters/1/unsubscribe/',
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'
        )
        self.assertEqual(len(newsletter.subs.all()), 0)
        self.assertEqual(response.status_code, 204)

    def test_invite_newsletter(self):
        User.objects.create_superuser(username='admin3', email='admin3@gmail.com', password='admin3')
        self.client.post(
              f'{self.host}/newsletters/',
              data={"name": "test2", "description": "this is a test2", "tags": [1], "target": 1, "frequency": 28},
              HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )
        response = self.client.post(
            f'{self.host}/newsletters/1/invite/',
            data={"admins": [3]},
            HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )
        
        self.assertEqual(len(Newsletter.objects.get(id=1).admins.all()), 2)
        self.assertEqual(response.status_code, 201)

    def test_edit_newsletter(self):
        self.client.post(
              f'{self.host}/newsletters/',
              data={"name": "test2", "description": "this is a test2", "tags": [1], "target": 1, "frequency": 28},
              HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )
        response = self.client.patch(
            f'{self.host}/newsletters/1/edit/',
            data={"name": "test4"},
            HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )

        self.assertEqual(Newsletter.objects.get(id=1).name, 'test4')
        self.assertEqual(response.status_code, 200)
