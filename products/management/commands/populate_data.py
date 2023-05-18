import json

from django.core.management.base import BaseCommand
from products.models import Brand, Category, Product, Sku, Media

class Command(BaseCommand):
    help = 'Populate data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='The JSON file to read data from')

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
                    category.save(update_fields=['parent'])

                parent_category_name = category_name

            brand, _ = Brand.objects.get_or_create(name=product['brand'].lower())
            category, _ = Category.objects.get_or_create(name=product['category'][-1])
            item = Product.objects.create(
                brand = brand,
                category = category,
                name = product['name'],
                market = product['market'],
                gender = product['gender'],
                care = ", ".join(product['care']),
                retail_id = product['retailer_sku'],
                description = product['description'],
            )

            media_to_bulk_create = []
            skus_to_bulk_create = []
            
            for image_url in product['image_urls']:
                image_data = {
                    'image_url': image_url,
                }
                media = Media(product=item, **image_data)
                media_to_bulk_create.append(media)

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
            Media.objects.bulk_create(media_to_bulk_create)

        self.stdout.write(self.style.SUCCESS('Data successfully populated'))
