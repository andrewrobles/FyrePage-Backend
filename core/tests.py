from django.test import TestCase

from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from .models import Link

class AuthTestCase(APITestCase):

    def setUp(self):
        self.username = 'fyre'
        self.password = '4321'

        self.response = self.client.post(
            'http://localhost:8000/core/users/', 
            {
                'username': self.username,
                'password': self.password
            }
        )

        self.token = self.response.data['token']

    def test_sign_up(self):
        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data['username'], self.username)
        self.assertTrue('token' in self.response.data)

    def test_current_user_while_signed_in(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        response = self.client.get('http://localhost:8000/core/current_user/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.username)

    def test_current_user_not_signed_in(self):
        response = self.client.get('http://localhost:8000/core/current_user/')

        self.assertEqual(response.status_code, 401)
        self.assertTrue('detail' in response.data)

    def test_log_in(self):
        response = self.client.post(
            'http://localhost:8000/token-auth/',
            {
                'username': self.username,
                'password': self.password
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user'], {'username': self.username})
        self.assertTrue('token' in response.data)


class LinksTestCase(APITestCase):

    def setUp(self):
        self.username = 'fyre'
        self.password = '4321'

        self.response = self.client.post(
            'http://localhost:8000/core/users/', 
            {
                'username': self.username,
                'password': self.password
            }
        )

        self.token = self.response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
    

    def test_post_link(self):
        url = 'http://localhost:8000/token-auth/'
        data = {
            'text': 'my link text',
            'url': 'my link url'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)

        user = response.user
        links = Link.objects.filter(user=user)

        self.assertEqual(len(links), 1)

        link = links.first()

        self.assertEqual(link.text, data['text'])
        self.assertEqual(link.url, data['url'])
