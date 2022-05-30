import random
from django.core.management.base import BaseCommand
from faker import Faker
import logging
from apps.categories.models import Categories
from apps.product.models import Manufactures, Products



logging.getLogger('faker').setLevel(logging.ERROR)
class Command(BaseCommand):

    help = "Command informations"

    def handle(self, *args, **kwargs):
        fake = Faker()

        print('======================== Stard Products DB Seed process =======================')
        for i in range(0,1000):
            name = fake.name()
            if Products.objects.filter(name__contains=name).count() == 0:
                rand_category = Categories.objects.order_by('?').first()
                rand_manufacture = Manufactures.objects.filter(group__exact=rand_category.type_id).order_by('?').first()
                
                product = Products()
                product.name             = name
                product.description      = fake.paragraph(nb_sentences=15) #optional
                discount_type            = product.discount_type = random.randrange(1,4)
                product_price            = product.price  = float(random.randrange(100,1000))
                if discount_type == 2:
                    product.discount     = random.randrange(10,30)
                elif discount_type == 3 :
                    product.discounted_price  = float(product.price - random.randrange(20, (product_price)//2))

                product.sku              = fake.swift(length=11)
                product.barcode          = fake.ean(length=13)
                product.quantity         = int(random.randrange(20,60))
                
                product.is_backorders    = random.randrange(0,2)

                is_physical = product.is_physical = random.randrange(0,2)
                if is_physical == 1:
                    product.weight           = random.randrange(5,100)
                    product.width            = random.randrange(50,500)
                    product.height           = random.randrange(50,500)
                    product.length           = random.randrange(50,500)

                status = product.status  = random.randrange(1,5)
                if status == 3:
                    product.publishing_date  = fake.future_datetime()

                product.category_id      = rand_category.id
                product.group_id         = rand_category.type_id
                product.manufacture_id   = rand_manufacture.id
                product.owner_id         = 1
                product.save()

        print('======================== End Products DB Seed process =======================')