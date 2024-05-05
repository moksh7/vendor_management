from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from vendor_management.models import Vendor


class TestVendorCrud(TestCase):
    def setUp(self):
        self.patcher = patch('vendor_management.views.vendor_list_create_view.IsAuthenticated.has_permission', return_value=True)
        self.patcher.start()
        for i in range(1, 6):
            Vendor.objects.create(id=i, name=f'vendor - {i}', vendor_code=f'VC{i}')

    def test_vendor_list(self):
        url = reverse('vendor_list_create')
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 5)

    def test_vendor_create(self):
        url = reverse('vendor_list_create')
        data = {
            'name': 'test vendor'
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.last().name, data['name'])

    def test_vendor_detail(self):
        url = reverse('vendor_detail_update', args=[1])
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['id'], 1)

    def test_vendor_update(self):
        url = reverse('vendor_detail_update', args=[1])
        data = {
            'address': 'test address'
        }
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.get(id=1).address, data['address'])

    def test_vendor_delete(self):
        url = reverse('vendor_detail_update', args=[1])
        self.client.delete(url)
        self.assertEqual(Vendor.objects.all().count(), 4)

    def test_vendor_performance(self):
        updates = {
            'on_time_delivery_rate': 100,
            'quality_rating_avg': 4,
            'average_response_time': 1,
            'fulfillment_rate': 50
        }
        Vendor.objects.filter(id=1).update(**updates)

        url = reverse('vendor_performance', args=[1])
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['on_time_delivery_rate'], updates['on_time_delivery_rate'])
        self.assertEqual(response_data['quality_rating_avg'], updates['quality_rating_avg'])
        self.assertEqual(response_data['average_response_time'], updates['average_response_time'])
        self.assertEqual(response_data['fulfillment_rate'], updates['fulfillment_rate'])

    def tearDown(self):
        self.patcher.stop()
