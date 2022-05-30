from random import random
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from apps.groups.models import Groups
from apps.users.models import Users
# Create your models here.

def category_image(self,filename):
    return f"category/banner/{self.id}/{self.name}-{random()}.png"

def category_default_image():
    return f"default/blank-image.svg"

def category_icon_image(self,filename):
    return f"category/icon/{self.id}/{self.name}-{random()}.png"

def category_icon_default_image():
    return f"default/blank-image.svg"




class Categories(models.Model):
    name = models.CharField(_('Name'),max_length=255,null=True, blank=True)
    slug = models.SlugField(_('Slug'), unique=True, editable=False)
    description = models.TextField(_('Description') , null=True, blank=True)
    icon = models.ImageField(_('Icon'), upload_to=category_icon_image, default=category_icon_default_image, null=True, blank=True)
    image = models.ImageField(_('Image'), upload_to=category_image, default=category_default_image, null=True, blank=True)
    type = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='+')
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='+')
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='child_category', verbose_name=_('child_category'), blank=True, null=True,)
    is_active = models.BooleanField(_('Is Active'),default=0)
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'


    def save(self, *args, **kwargs):  # new
        if not self.slug or self.name:
            self.slug = slugify(str(self.name))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name