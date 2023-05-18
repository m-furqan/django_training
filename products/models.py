from django.db import models
from mixins.timestamp_mixin import TimestampMixin
from enum import Enum


class Gender(Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'


class Brand(TimestampMixin):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(TimestampMixin):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(TimestampMixin):
    care = models.TextField()
    description = models.TextField()
    name = models.CharField(max_length=200)
    market = models.CharField(max_length=100)
    retail_id = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=[(gender.value, gender.name) for gender in Gender])
    
    def __str__(self):
        return self.name


class Sku(TimestampMixin):
    size = models.CharField(max_length=20)
    colour = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)
    is_out_of_stock = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='skus')

    def __str__(self):
        return f"{self.product.name} - {self.colour} - {self.size}"

class Media(TimestampMixin):
    image_url = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media')

    def __str__(self):
        return self.image_url
