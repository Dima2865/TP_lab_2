from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Purchase, Customers
from shop.views import calculate_discounts_for_customers, subtract_percent


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=100)
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/index.html')
        self.assertContains(response, self.product.name)


class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=100)
        self.client = Client()
        self.data = {'product': self.product.id, 'person': 'Test Person', 'address': 'Test Address'}

    def test_purchase_create_view_get(self):
        response = self.client.get(reverse('buy', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_purchase_create_view_post(self):
        response = self.client.post(reverse('buy', args=[1]), self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(Customers.objects.count(), 1)

    def test_discount_application_for_new_customer(self):
        # Проверяем, что скидка не применяется для нового покупателя
        data = {'product': self.product.id, 'person': 'New Customer', 'address': 'New Address'}
        self.client.post(reverse('buy', args=[0]), data)

        purchase = Purchase.objects.get(person='New Customer')
        self.assertEqual(purchase.final_price, 100.0)

        customer = Customers.objects.get(name='New Customer')
        self.assertEqual(customer.purchase_count, 1)
        self.assertEqual(customer.discount, 0)

    def test_discount_application_for_existing_customer(self):
        # Проверяем, что скидка применяется для существующего покупателя
        Customers.objects.create(name="Existing Customer", purchase_count=6, discount=5)
        data = {'product': self.product.id, 'person': 'Existing Customer', 'address': 'Existing Address'}
        self.client.post(reverse('buy', args=[0]), data)

        purchase = Purchase.objects.get(person='Existing Customer', product=self.product)
        self.assertAlmostEqual(purchase.final_price, 95.0)

        customer = Customers.objects.get(name='Existing Customer')
        self.assertEqual(customer.purchase_count, 7)
        self.assertEqual(customer.discount, 5)

    def test_discount_application_for_high_purchase_count(self):
        # Проверяем, что скидка 10% применяется для покупателя с более чем 10 покупками
        Customers.objects.create(name="High Purchase Customer", purchase_count=11, discount=10)
        data = {'product': self.product.id, 'person': 'High Purchase Customer', 'address': 'High Purchase Address'}
        self.client.post(reverse('buy', args=[0]), data)

        purchase = Purchase.objects.get(person='High Purchase Customer', product=self.product)
        self.assertAlmostEqual(purchase.final_price, 90.0)

        customer = Customers.objects.get(name='High Purchase Customer')
        self.assertEqual(customer.purchase_count, 12)
        self.assertEqual(customer.discount, 10)


class CustomersListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        Customers.objects.create(name="Customer1", purchase_count=3, discount=0)
        Customers.objects.create(name="Customer2", purchase_count=7, discount=5)
        Customers.objects.create(name="Customer3", purchase_count=12, discount=10)

    def test_customers_list_view(self):
        response = self.client.get(reverse('customers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/customers_form.html')
        self.assertContains(response, "Customer1")
        self.assertContains(response, "Customer2")
        self.assertContains(response, "Customer3")

    def test_discounts_calculation(self):
        # Проверяем, что скидки рассчитываются правильно
        calculate_discounts_for_customers()

        customer1 = Customers.objects.get(name="Customer1")
        customer2 = Customers.objects.get(name="Customer2")
        customer3 = Customers.objects.get(name="Customer3")

        self.assertEqual(customer1.discount, 0)
        self.assertEqual(customer2.discount, 5)
        self.assertEqual(customer3.discount, 10)

    def test_calculate_discounts_for_customers_with_no_purchases(self):
        # Проверяем, что скидки устанавливаются в 0 для покупателей с нулевым количеством покупок
        Customers.objects.create(name="Customer4", purchase_count=0, discount=5)
        calculate_discounts_for_customers()

        customer4 = Customers.objects.get(name="Customer4")
        self.assertEqual(customer4.discount, 0)
