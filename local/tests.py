from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status, permissions
from django.contrib.auth.models import User
from .models import FirebaseToken
from django.urls import reverse

# Create your tests here.

class FirebaseTokenViewTestCase(APITestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create(username='testuser', email='testuser@email.com', password='password123')
        cls.username = 'testuser'
        cls.email = 'testuser@email.com'
        cls.firebase_uid = "5X8umdTlIIe5Rk1Z13sLu4X8iWm2"
        cls.token_str = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU2OTFhMTk1YjI0MjVlMmFlZDYwNjMzZDdjYjE5MDU0MTU2Yjk3N2QiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZmItdGVzdC1lM2ZlNiIsImF1ZCI6ImZiLXRlc3QtZTNmZTYiLCJhdXRoX3RpbWUiOjE3MjA3NTA4NDEsInVzZXJfaWQiOiI1WDh1bWRUbElJZTVSazFaMTNzTHU0WDhpV20yIiwic3ViIjoiNVg4dW1kVGxJSWU1UmsxWjEzc0x1NFg4aVdtMiIsImlhdCI6MTcyMDc1MDg0MSwiZXhwIjoxNzIwNzU0NDQxLCJlbWFpbCI6InRlc3R1c2VyQGVtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJ0ZXN0dXNlckBlbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.cRN2I48DdNA0DvLzeKjPROuYsyEb0P1s91gHJ1aVIgsxSRYqf8wBxHiH14zfF6Uttx6Eym-KC2b97Kzc--ATh6EUqvGzbaHW_uCbDkCesBoE0r89Ap2aUe2S-HKgWoiWa-_2Ok6dboo_odMVIN2VIK_zmeyM4-kOpqckF1O7HkbQdf8aKQDKHiQDY4RQVUMChupPCrH5FnVIxXrKaNI23iW98ddpitc-uON-BjezLbkRuorXZlP3kqYg-FzxRwHMapaSLAYsJZEITwhIteHW1JxyCAthhQuLdXWD-S1vIBzjGqMDgfLf7mn7idk0vfxJSjxDmGAocvDiRQvosBcSfg"
        # need to update token_str

    def test_post_valid_token(self):
        url = reverse('firebase-token-list')
        data = {'token': self.token_str, 'username': self.username}
        #self.client.credentials(HTTP_AUTHORIZATION=f'{token}')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], self.user.pk)
        self.assertEqual(response.data['firebase_uid'], self.firebase_uid)
        self.assertEqual(response.data['is_active'], True)


    def test_delete_valid_token(self):
        url = reverse('firebase-token-list')
        data = {'token': self.token_str, 'username': self.username}
        response = self.client.post(url, data, format='json')
        #self.client.credentials(HTTP_AUTHORIZATION=f'{token}')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

