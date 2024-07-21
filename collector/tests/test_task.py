from unittest.mock import patch
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from ..models.collections_model import Collection
from ..serializers.tasks_serializer import CollectionSerializer
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework import status
User = get_user_model()


class CollectionFilterTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
        )

        # Create some collections with different statuses and dates
        self.collection1 = Collection.objects.create(
            user=self.user,
            amount=3000,
            status='collected',
            collectionDate=timezone.now() - timedelta(hours=24)
        )
        self.collection2 = Collection.objects.create(
            user=self.user,
            amount=2500,
            status='pending',
            collectionDate=timezone.now() - timedelta(hours=24)
        )
        self.collection3 = Collection.objects.create(
            user=self.user,
            amount=7000,
            status='pending',
            collectionDate=timezone.now() - timedelta(hours=24)
        )

        # Set min_amount in settings for testing
        self.min_amount = 5000
        self.min_hours = 48
        settings.MIN_AMOUNT = self.min_amount
        settings.MIN_HOURS = self.min_hours

        self.client = Client()
        self.client.login(username='testuser', password='password')

    def test_UserDoneTasks(self):
        url = f'/user-tasks/{self.user.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '3000')
        self.assertNotContains(response, '2500')
        self.assertNotContains(response, '7000')  

    def test_UserNextTask(self):
        url = f'/user-next-task/{self.user.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2500')



    def test_collect_task_collection_not_found(self):
        url = reverse('collect_task', args=[999])  # Assuming 999 is an invalid ID
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Collection Item not found')

    def test_collect_check_status(self):
        url = f'/check-status/{self.user.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 202)


    def test_payTask(self):
        url = f'/pay/{self.collection2.pk}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 202)




    @patch('collector.views.tasks.checkUserStatusApi', return_value=406)  
    def test_account_frozen(self, mock_check_status):
        url = reverse('collect_task', kwargs={'task_id': self.collection2.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data['message'], 'account is Frozen!')



    @patch('collector.views.tasks.checkUserStatusApi', return_value=202)
    def test_collection_successful(self, mock_check_status):
        url = reverse('collect_task', kwargs={'task_id': self.collection2.pk})
        response = self.client.post(url)
        self.collection2.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(self.collection2.status, 'collected')
        self.assertIsNotNone(self.collection2.collectionDate)
        expected_data = CollectionSerializer(self.collection2).data
        self.assertEqual(response.data, expected_data)
        mock_check_status.assert_called_once_with(self.collection2.user)