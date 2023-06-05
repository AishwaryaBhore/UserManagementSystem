from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from managementapi.models import CustomUser


class CustomUserAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='ranu', date_of_birth='1999-09-09', password='12334',
                                                   email='ranu@gmail.com', phone_number='7778889956',
                                                   street='shahu colony', zip_code='12345', city='mumbai', country='uk',
                                                   state='kerla')
        self.data_post_success = {
            'username': 'manu',
            'password': '123',
            'email': 'ab@gmail.com',
            'date_of_birth': '2034-02-01',
            'phone_number': '9623425988',
            'street': 'shahu colony',
            'zip_code': 412341,
            'city': 'vashi',
            'country': 'india',
            'state': 'maha',

        }
        self.data_post_fail = {
            'username': 'manisha',
            'email': 'cd@gmail.com',
        }

    def test_user_info(self):
        """"This is method to test info of users"""
        qs = CustomUser.objects.all()
        self.assertEqual(qs.count(), 1)
        e1 = CustomUser.objects.get(username='ranu')
        self.assertEqual(e1.username, 'ranu')

    def test_post_method_success(self):
        """"This is method to test create API works successfully"""
        response = self.client.post((reverse('user_post')), self.data_post_success, format='json')
        self.assertEqual(response.status_code, 201)

    def test_post_method_fail(self):
        """"This is method to test working of create API  works by providing insufficient credentials """
        response = self.client.post((reverse('user_post')), self.data_post_fail, format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_method_success(self):
        """This is method to test working of delete API for success"""
        self.client.login(username='ranu', password='12334')
        response = self.client.delete(reverse('user_delete', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_method_fail(self):
        """"This is method to test working of delete API for fail"""
        self.client.login(username='ranu', password='12334')
        response = self.client.put(reverse('user_update', kwargs={'pk': 23}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_method_success(self):
        """This is method to test working of retrieve API for success"""
        self.client.login(username='ranu', password='12334')
        response = self.client.get(reverse('user_update', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_method_fail(self):
        """"This is method to test working of retrieve API for fail"""
        self.client.login(username='ranu', password='12334')
        response = self.client.get(reverse('user_update', kwargs={'pk': 34}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

