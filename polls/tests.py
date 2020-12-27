# from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from polls import apiviews

# Create your tests here.

class TestPoll(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.view = apiviews.PollViewSet.as_view({'get':'list'})
        self.uri = '/polls/'
        self.user = self.setup_user()
        #print(self.user)
        self.token = Token.objects.create(user=self.user)
        #print(self.token)
        self.token.save()
    
    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            username='test',
            email='test@test.com',
            password='citrix2010'
        )
    
    def test_list(self):
        request = self.factory.get(
            self.uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
            )
        response = self.view(request)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead'.format(response.status_code))
    
    def test_list2(self):
        # print(f'username={self.user.username}, passowrd={self.user.password}')
        self.client.login(username=self.user.username, password='citrix2010')
        response = self.client.get(
            self.uri
        )
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead'.format(response.status_code)) 
    
    def test_createpoll(self):
        # print(f'username={self.user.username}, passowrd={self.user.password}')
        self.client.login(username=self.user.username, password='citrix2010')
        params = {
            "question": "SAT or ACT?",
            "created_by": 1
        }
        response = self.client.post(
            self.uri,
            params
        )
        self.assertEqual(response.status_code, 201, 'Expected Response Code 201, received {0} instead'.format(response.status_code))               