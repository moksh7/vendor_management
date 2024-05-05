from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from vendor_management.models import Vendor, PurchaseOrder, HistoricalPerformance


class TestVendorCrud(TestCase):
    def setUp(self):
        self.patcher = patch('vendor_management.views.po_list_create_view.IsAuthenticated.has_permission', return_value=True)
        self.patcher.start()
        self.vendor = Vendor.objects.create(id=1, name='vendor - 1', vendor_code=f'VC01')
        for i in range(1, 4):
            PurchaseOrder.objects.create(id=i, po_number=f'PO{i}', items={'key': 'test_item'}, quantity=i, vendor=self.vendor)

    def test_po_list(self):
        url = reverse('po_list_create')
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 3)

    def test_po_create(self):
        url = reverse('po_list_create')
        data = {
            'vendor': self.vendor.id,
            'items': {'key': 'test_item'},
            'quantity': 2
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.all().count(), 4)

    def test_po_detail(self):
        url = reverse('po_detail_update', args=[1])
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['id'], 1)

    def test_po_delete(self):
        url = reverse('po_detail_update', args=[1])
        self.client.delete(url)
        self.assertEqual(PurchaseOrder.objects.all().count(), 2)

    def test_ack_po(self): 
        url = reverse('po_acknowledge', args=[1])
        response = self.client.post(url)
        self.vendor.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.vendor.average_response_time, 0)

    def test_update_po(self):
        url = reverse('po_detail_update', args=[1])
        data = {
            'est_delivery_date': '2024-05-10',
            'delivery_date': '2024-05-07',
            'status': 'completed',
            'quality_rating': 4
        }
        response = self.client.put(url, data, content_type='application/json')
        self.vendor.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.vendor.quality_rating_avg, 4)
        self.assertEqual(self.vendor.on_time_delivery_rate, 100)
        self.assertEqual(int(self.vendor.fulfillment_rate), 33)
