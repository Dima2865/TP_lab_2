from django.db import models

<<<<<<< HEAD

=======
>>>>>>> 44d0611050b99de89b5a3c815e64bc1c2e90152d
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

<<<<<<< HEAD

=======
>>>>>>> 44d0611050b99de89b5a3c815e64bc1c2e90152d
class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    final_price = models.FloatField(null=True, default=0.0)

<<<<<<< HEAD

=======
>>>>>>> 44d0611050b99de89b5a3c815e64bc1c2e90152d
class Customers(models.Model):
    name = models.CharField(max_length=200)
    purchase_count = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
