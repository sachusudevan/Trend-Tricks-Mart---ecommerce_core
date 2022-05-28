from random import  random, randrange
from django.core.management.base import BaseCommand
from faker import Faker
import logging

from apps.shops.models import Shops



logging.getLogger('faker').setLevel(logging.ERROR)
class Command(BaseCommand):

    help = "Command informations"

    def handle(self, *args, **kwargs):
        fake = Faker()

        print('======================== Stard Shop DB Seed process =======================')

        for i in range(0,30):
            shop = Shops()
            #general
            shop.name              = fake.company()
            shop.description       = fake.paragraph(nb_sentences=25) #optional
            shop.country_id        = 1
            shop.state_id          = randrange(1,25)
            shop.city              = fake.city()
            shop.zip_code          = fake.postcode()
            shop.street_address    = fake.address()

            #advanced  #optional
            shop.account_holder_name   = fake.name()
            shop.account_holder_email  = fake.ascii_safe_email()
            shop.bank_name             = fake.company()
            shop.account_number        = fake.bban()
            shop.latitude              = fake.latitude()
            shop.longitude             = fake.longitude()
            shop.contact_number        = fake.phone_number()
            shop.website               = fake.uri()

            # self.meta_title            = request.POST.get('meta_title','').strip()
            # self.shop_meta_description = request.POST.get('shop_meta_description','').strip()
            # self.meta_keywords         = request.POST.get('meta_keywords','').strip()

            shop.is_active               = 1
            shop.owner_id = 1
            shop.save()


        print('======================== End Shop DB Seed process =======================')