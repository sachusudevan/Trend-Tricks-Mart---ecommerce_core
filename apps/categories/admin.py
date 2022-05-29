from django.contrib import admin
from .models import Categories

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    model = Categories
    list_display = ['name','icon','image','slug','owner','type_id','parent_category_id', 'is_active','created_date','modified_date']
    list_display_links = ['name']

admin.site.register(Categories,CategoryAdmin)