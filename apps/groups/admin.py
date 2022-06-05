from django.contrib import admin

from .models import Groups
# Register your models here.
class GroupsAdmin(admin.ModelAdmin):
    model = Groups
    list_display = ['name','icon','banner','slug','is_main_homepage','owner','layout', 'is_active','created_date','modified_date']
    list_display_links = ['name']
    search_fields = ('name',)

admin.site.register(Groups,GroupsAdmin)