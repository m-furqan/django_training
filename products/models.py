from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    retail_id = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    brand = models.CharField(max_length=100)
    market = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    description = models.TextField()
    care = models.TextField()
    image_urls = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Sku(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='skus')
    is_out_of_stock = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=20)
    colour = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.colour} - {self.size}"
