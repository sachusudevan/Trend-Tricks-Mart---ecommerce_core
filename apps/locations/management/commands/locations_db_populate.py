import sys
from datetime import datetime
from time import sleep, gmtime, strftime
from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.models import User
import pycountry
from apps.locations.models import Country, State


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        india = [pycountry.countries.get(alpha_2='IN')]

        self.loadCountry(india)
        
        self.stdout.write("\n")
        self.stdout.write("Process Completed....")

    def loadCountry(self,data):
        for country in data:
            country_data = Country()
            country_data.country_name = country.name
            country_data.code = country.alpha_2
            country_data.country_code = country.alpha_3
            country_data.save()

            if len(pycountry.subdivisions.get(country_code=country.alpha_2)) > 1 :
                for state in pycountry.subdivisions.get(country_code=country.alpha_2) :
                    state_data = State()
                    state_data.state_name = state.name
                    state_data.state_code = state.code
                    state_data.state_type = state.type
                    state_data.country_id  = country_data.id
                    state_data.save()

                    