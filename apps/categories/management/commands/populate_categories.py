from random import  random, randrange
from django.core.management.base import BaseCommand
from faker import Faker
import logging
from apps.categories.models import Categories
from apps.groups.models import Groups


logging.getLogger('faker').setLevel(logging.ERROR)
class Command(BaseCommand):

    help = "Command informations"

    def handle(self, *args, **kwargs):
        fake = Faker()

        print('======================== Stard category DB Seed process =======================')

        for i in range(0,30):
            name = fake.company()
            if Categories.objects.filter(name__contains=name).count() == 0:
                group = Groups.objects.order_by('?').first()
                rand_category = Categories.objects.order_by('?').first()
                category = Categories()
                category.name              = name
                category.description       = fake.paragraph(nb_sentences=25) #optional
                category.country_id        = 1
                category.state_id          = randrange(1,25)
                category.city              = fake.city()
                category.zip_code          = fake.postcode()
                category.street_address    = fake.address()

                category.is_active         = 1
                category.type_id           = group.id
                category.owner_id = 1
                category.parent_category_id  = None if rand_category is None else rand_category.id
                category.save()


        print('======================== End category DB Seed process =======================')