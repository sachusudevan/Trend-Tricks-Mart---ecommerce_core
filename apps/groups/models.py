from random import random
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from apps.users.models import Users
# Create your models here.


def groups_banner_image(self,filename):
    return f"groups/banner/{self.name}-{random()}.png"

def groups_banner_default_image():
    return f"default/blank-image.svg"

def groups_icon_image(self,filename):
    return f"groups/icon/{self.name}-{random()}.png"

def groups_icon_default_image():
    return f"default/blank-image.svg"



class Groups(models.Model):
    name = models.CharField(_('Name'),max_length=255,null=True, blank=True)
    slug = models.SlugField(_('Slug'), unique=True, editable=False)
    icon = models.ImageField(_('Icon'), upload_to=groups_icon_image, default=groups_icon_default_image, null=True, blank=True)
    banner = models.ImageField(_('Banner'), upload_to=groups_banner_image, default=groups_banner_default_image, null=True, blank=True)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='+')
    is_main_homepage = models.BooleanField(_('Is Main Homepage'),default=0)
    layout = models.IntegerField(_('Layout'),default=1, help_text="1 => Classic, 2 => Compact, 3 => Minimal, 4 => Modern, 5 => Standard, " )
    is_active = models.BooleanField(_('Is Active'),default=0)
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)


    class Meta:
        ordering = ('name',)
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(str(self.name))
        return super().save(*args, **kwargs)


    def __str__(self):
        return '{}'.format(self.name)







