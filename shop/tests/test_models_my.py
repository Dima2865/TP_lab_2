from django.test import TestCase
from shop.models import Customers


class CustomersTestCase(TestCase):
    def setUp(self):
        self.customer = Customers.objects.create(name="Petrov", purchase_count=3, discount=0)

    def test_correctness_types(self):
        self.assertIsInstance(self.customer.name, str)
        self.assertIsInstance(self.customer.purchase_count, int)
        self.assertIsInstance(self.customer.discount, int)

    def test_correctness_data(self):
        self.assertTrue(self.customer.name == "Petrov")
        self.assertTrue(self.customer.purchase_count == 3)
        self.assertTrue(self.customer.discount == 0)
