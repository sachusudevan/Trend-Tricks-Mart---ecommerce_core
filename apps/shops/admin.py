from django.contrib import admin

from apps.shops.models import Shops



class CountryAdmin(admin.ModelAdmin):
    model = Shops
    list_display = [ 'name','logo','slug','country','owner','state', 'is_active','created_date','modified_date']
    list_display_links = ['name']

admin.site.register(Shops,CountryAdmin)