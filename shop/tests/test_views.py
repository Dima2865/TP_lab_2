from django.test import TestCase, Client
from shop.views import PurchaseCreate

<<<<<<< HEAD

=======
>>>>>>> 44d0611050b99de89b5a3c815e64bc1c2e90152d
class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_webpage_accessibility(self):
        response = self.client.get('/')
<<<<<<< HEAD
        self.assertEqual(response.status_code, 200)
=======
        self.assertEqual(response.status_code, 200)
>>>>>>> 44d0611050b99de89b5a3c815e64bc1c2e90152d
