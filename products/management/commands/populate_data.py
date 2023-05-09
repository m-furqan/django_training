import json
import random

from django.core.management.base import BaseCommand, CommandError
from products.models import Category, Inventory, Product

class Command(BaseCommand):
    help = 'Populate data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='The JSON file to read data from')

    def handle(self, *args, **options):
        filename = options['filename']
        with open(filename, 'r') as file:
            data = json.load(file)
        
        for product in data:
            category = Category.objects.create(name=product['category'][0])
            inventory = Inventory.objects.create(quantity=random.randint(1, 100))
            
            Product.objects.create(
                name=product['name'],
                description=product['description'],
                category_id=category,
                inventory_id=inventory,
                price=product['price']
            )
        self.stdout.write(self.style.SUCCESS('Data successfully populated'))
