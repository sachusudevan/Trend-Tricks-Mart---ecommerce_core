from django.contrib import admin
from django.contrib.auth.models import PermissionsMixin
from apps.users.models import UserRole, Users
from django.forms import TextInput, Textarea
from django.utils.translation import gettext as _
from django.contrib.auth.models import Permission



class UsersAdmin(admin.ModelAdmin):
    model = Users
    list_display = ['id', 'email','first_name','last_name','username','phone']
    list_display_links = ['email']
    
    fieldsets = (
        ("Profile", {'fields': ('email', 'first_name','last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_admin','is_superuser','is_verified','groups','user_permissions')}),
        ('Personal', {
            'fields': ('username','phone','company','dob','gender','otp','landmark')
            }),
    )

    
    search_fields = ('email', 'first_name','last_name')
    ordering = ('email',)
    filter_horizontal = ()
    
    formfield_overrides = {
        Users.bio: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }

admin.site.register(Users,UsersAdmin)


class UserRoleAdmin(admin.ModelAdmin):
    model = Users
    list_display = ['user', 'cutomer_type','created_date','modified_date']
    list_display_links = ['cutomer_type']
    
admin.site.register(UserRole,UserRoleAdmin)
