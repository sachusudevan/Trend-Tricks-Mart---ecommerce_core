import random
from django.core.management.base import BaseCommand
from faker import Faker
import logging

from apps.groups.models import Groups



logging.getLogger('faker').setLevel(logging.ERROR)
class Command(BaseCommand):

    help = "Command informations"

    def handle(self, *args, **kwargs):
        fake = Faker()

        groups = ['Daily Needs','Grocery','Toys','Furniture','Books','Clothing','Bags','Makeup','Bakery','TV','Smart Phones','Laptops','Electronics']

        print('======================== Stard group DB Seed process =======================')

        for i in range(0,30):
            name = random.choice(groups)
            if Groups.objects.filter(name__contains=name).count() == 0:
                group = Groups()
                #general
                group.name              = name
                group.is_main_homepage  = 1
                group.layout            = random.randrange(1,5)
                group.is_active         = 1
                group.owner_id          = 1
                group.save()


        print('======================== End group DB Seed process =======================')