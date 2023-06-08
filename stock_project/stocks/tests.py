from django.test import TestCase
from rest_framework.test import APIClient


class BuyStockAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Set up your test data and Redis data if needed

    def test_buy_stock_accept(self):
        data = {
            'user': 'some_user',
            # Other required data for the request
        }

        response = self.client.post('/buy-stock/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Accept')

    def test_buy_stock_deny(self):
        data = {
            "user": "user2",
            "stockname": "stock1",
            "quantity": 1000
        }
        response = self.client.post('/buy-stock/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Deny')
