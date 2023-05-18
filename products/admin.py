from django.contrib import admin

from .models import Product, Brand, Category, Sku, Media


admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Sku)
admin.site.register(Media)