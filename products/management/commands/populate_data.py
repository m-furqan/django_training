import json
import random

from django.core.management.base import BaseCommand
from products.models import Category, Product, Sku

class Command(BaseCommand):
    help = 'Populate data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='The JSON file to read data from')

    # def create_or_return_category(self, category_name):
    #     try:
    #         category = Category.objects.get(name=category_name)
    #         return category

    #     except Category.DoesNotExist:
    #         return Category.objects.create(name=category_name)

    def handle(self, *args, **options):
        filename = options['filename']
        with open(filename, 'r') as file:
            data = json.load(file)
        
        for product in data:
            parent_category_name = None

            for category_name in product['category']:
                category_name = category_name.lower()
                category, _ = Category.objects.get_or_create(name=category_name)

                if parent_category_name and not category.parent:
                    category.parent, _ = Category.objects.get_or_create(name=parent_category_name)
                    category.save()
                
                parent_category_name = category_name

            category, _ = Category.objects.get_or_create(name=product['category'][-1])
            item = Product.objects.create(
                retail_id = product['retailer_sku'],
                gender = product['gender'],
                brand = product['brand'],
                market = product['market'],
                name = product['name'],
                description = product['description'],
                care = ", ".join(product['care']),
                image_urls = product['image_urls'],
                category = category,
            )

            skus_to_bulk_create = []
            for sku in product['skus'].values():
                sku_data = {
                    'is_out_of_stock': sku.get('out_of_stock') or False,
                    'price': sku['price'],
                    'size': sku['size'],
                    'colour': sku.get('color') or 'UniColour',
                    'currency': sku['currency'],
                }
                sku = Sku(product=item, **sku_data)
                skus_to_bulk_create.append(sku)

            Sku.objects.bulk_create(skus_to_bulk_create)

        self.stdout.write(self.style.SUCCESS('Data successfully populated'))
