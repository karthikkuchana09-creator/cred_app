from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthTests(APITestCase):
    def test_register_login(self):
        url = reverse('register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'Test@1234'}
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        login_url = reverse('token_obtain_pair')
        res = self.client.post(login_url, {'email': data['email'], 'password': data['password']}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)


class CardManagementTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='carduser', email='card@example.com', password='Card@1234')
        self.token = self.client.post(reverse('token_obtain_pair'), {'email': self.user.email, 'password': 'Card@1234'}, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_add_and_list_card(self):
        url = reverse('cards')
        res = self.client.post(url, {'raw_number': '4111111111111111', 'card_type': 'VISA'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['last4'], '1111')

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_delete_card(self):
        res = self.client.post(reverse('cards'), {'raw_number': '4111111111111111', 'card_type': 'VISA'}, format='json')
        card_id = res.data['id']
        res = self.client.delete(reverse('delete_card', kwargs={'pk': card_id}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
