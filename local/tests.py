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
        cls.firebase_uid = '5X8umdTlIIe5Rk1Z13sLu4X8iWm2'
        cls.token_str = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjU2OTFhMTk1YjI0MjVlMmFlZDYwNjMzZDdjYjE5MDU0MTU2Yjk3N2QiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZmItdGVzdC1lM2ZlNiIsImF1ZCI6ImZiLXRlc3QtZTNmZTYiLCJhdXRoX3RpbWUiOjE3MjA2NzcyMjQsInVzZXJfaWQiOiI1WDh1bWRUbElJZTVSazFaMTNzTHU0WDhpV20yIiwic3ViIjoiNVg4dW1kVGxJSWU1UmsxWjEzc0x1NFg4aVdtMiIsImlhdCI6MTcyMDY3NzIyNCwiZXhwIjoxNzIwNjgwODI0LCJlbWFpbCI6InRlc3R1c2VyQGVtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJ0ZXN0dXNlckBlbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.SmQmuknTpit5zDCvY74SPszHkdTdgtPartsZvhvBWVg5PP3dW5houllo9ZlV4TApRDI0jyVzwXAuRfp-pSJIsaZrwbjct7WjWaxclvyzz7JPVg6mBM3aKc3WVgvZmefBV1iQveijQx6xSCtjKMcrst3xsDhsWVyiqykuNYTVhmVYbnHe6lMdk3yGyb69sR5ufbqje03eSasnydYSocNLAb0NBPoBfWuoxHF_ejwGtE2EBhcfxG1hVMPOOCnmTZlbkTKkTor8LYYwN2jIDejFpm4U_XXMISQn_jZTEGWTQjGkqDhlHckVZGyr8MB3nemCmgeRVTkW_2kUo3yNia0Oig'

        cls.token = FirebaseToken.objects.create(
            user=cls.user,
            firebase_uid=cls.firebase_uid,
            token=cls.token_str
        )

    def post_valid_token(self):
        url = reverse('firebase-token-list')
        data = {'token': self.token_str}
        #self.client.credentials(HTTP_AUTHORIZATION=f'{token}')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['token'], self.token_str)


    def test_update_valid_token(self):
        url = reverse('firebase-token-list')
        data = {'token': self.token_str}
        #self.client.credentials(HTTP_AUTHORIZATION=f'{token}')
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['token'], self.token_str)

    def test_delete_valid_token(self):
        url = reverse('firebase-token-list')
        data = {'token': self.token_str}
        #self.client.credentials(HTTP_AUTHORIZATION=f'{token}')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

