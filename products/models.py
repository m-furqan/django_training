from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Inventory(models.Model):
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    inventory_id = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
