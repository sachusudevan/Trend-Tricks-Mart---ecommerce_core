import random
from django.core.management.base import BaseCommand
from faker import Faker
import logging
from apps.categories.models import Categories
from apps.product.models import Discount, Manufactures, ProductColor, ProductSize, Products
import randomcolor
import webcolors as wc

logging.getLogger('faker').setLevel(logging.ERROR)
class Command(BaseCommand):

    help = "Command informations"

    def handle(self, *args, **kwargs):
        fake = Faker()

        print('======================== Stard Products DB Seed process =======================')
        for i in range(0,500):
            name = fake.name()
            if Products.objects.filter(name__contains=name).count() == 0:
                rand_category = Categories.objects.order_by('?').first()
                rand_manufacture = Manufactures.objects.filter(group__exact=rand_category.type_id).order_by('?').first()
                
                product = Products()
                product.name             = name
                product.description      = fake.paragraph(nb_sentences=15) #optional
                product_price            = product.price  = float(random.randrange(100,1000))

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

                
                self.generateProductDiscount(product.id,product_price)
                self.generateProductColor(product.id)
                self.generateProductSize(product.id)
                



        print('======================== End Products DB Seed process =======================')

                


    def generateProductDiscount(self,product_id,product_price):
        discount = Discount()
        fake = Faker()
        discount.description     = fake.paragraph(nb_sentences=10)
        discount_type            = discount.discount_type = 2
        # discount_type            = discount.discount_type = random.randrange(1,4)
        if discount_type == 2:
            discount.discount  =   percentage    = random.randrange(10,30)
            discount.name            = "{price}% Discount on this product".format(price=percentage)
        elif discount_type == 3 :
            discount.discounted_price  = float(product_price - random.randrange(20, (product_price)//2))
            discount.name            = "Fixed Price"
        discount.product_id = product_id

        discount.is_active = 1
        discount.save()




    def generateProductColor(self,product_id):
        rand_color = randomcolor.RandomColor()
        for code in rand_color.generate(count= random.randrange(1,5)):
            
            try:
                color =  wc.hex_to_name(code)
            except Exception as e:
                color =  code

            product_color = ProductColor()
            product_color.product_id = product_id
            product_color.name     = "This product available in {color} variant".format(color=color)
            product_color.color_code    = code
            product_color.is_active = 1
            product_color.save()



    def generateProductSize(self,product_id):

        size_list = [
                [
                        {'name': "Euro 40", "size" : "6"},
                        {'name': "Euro 41", "size" : "7"},
                        {'name': "Euro 42", "size" : "8"},
                        {'name': "Euro 43", "size" : "9"},
                        {'name': "Euro 44", "size" : "10"}
                ],
                [
                        {'name': "Chest 38 inch | Length 26.5 inch | Shoulder 15 inch", "size" : "S"},
                        {'name': "Chest 40 inch | Length 27 inch | Shoulder 16 inch", "size" : "M"},
                        {'name': "Chest 42 inch | Length 28 inch | Shoulder 17 inch", "size" : "L"},
                        {'name': "Chest 44 inch | Length 29 inch | Shoulder 18 inch", "size" : "XL"},
                        {'name': "XXL", "size" : "XXL"}
                ]
            ]

        random_list = random.choice(size_list)
        for random_size in random_list:
            product_size = ProductSize()
            product_size.product_id = product_id
            product_size.name     = random_size['name']
            product_size.size     = random_size['size']
            product_size.is_active = 1
            product_size.save()

            