from django.contrib import admin

from apps.locations.models import Country, State

# Register your models here.


class CountryAdmin(admin.ModelAdmin):
    model = Country
    list_display = [ 'country_name','code','country_code','created_date','modified_date']
    list_display_links = ['country_name']

admin.site.register(Country,CountryAdmin)

class StateAdmin(admin.ModelAdmin):
    model = State
    list_display = ['state_name','state_code','country', 'state_type','created_date','modified_date']
    list_display_links = ['state_name']
    search_fields = ['state_name','state_code','country', 'state_type']

admin.site.register(State,StateAdmin)
