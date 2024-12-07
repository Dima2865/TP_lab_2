from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    final_price = models.FloatField(null=True, default=0.0)


class Customers(models.Model):
    name = models.CharField(max_length=200)
    purchase_count = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
