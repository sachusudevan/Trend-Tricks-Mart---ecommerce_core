from random import random
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from apps.users.models import Users
from apps.locations.models import Country, State

def shops_cover_image(self,filename):
    return f"shops/cover/{self.id}/{self.name}-{random()}.png"

def shops_cover_default_image():
    return f"default/default-shop-image.jpg"

def shops_logo_image(self,filename):
    return f"shops/logo/{self.id}/{self.name}-{random()}.png"

def shops_logo_default_image():
    return f"default/default-shop-logo.png"



class Shops(models.Model):
    name = models.CharField(_('Name'),max_length=255,null=True, blank=True)
    description = models.TextField(_('Description') , null=True, blank=True)
    logo = models.ImageField(_('Logo'), upload_to=shops_logo_image, default=shops_logo_default_image, null=True, blank=True)
    slug = models.SlugField(_('Slug'), unique=True, editable=False)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)

    cover_image = models.ImageField(_('Cover Image'), upload_to=shops_cover_image, default=shops_cover_default_image, null=True, blank=True)
    account_holder_name = models.CharField(_('Account Holder Name'), max_length=255,null=True, blank=True)
    account_holder_email = models.EmailField(_('Account Holder Email'), max_length=255, null=True, blank=True)
    bank_name = models.CharField(_('Bank Name'),max_length=255,null=True, blank=True)
    account_number = models.CharField(_('Account Number'),max_length=255,null=True, blank=True)

    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.CASCADE)
    city = models.CharField(_('City'),max_length=255,null=True, blank=True)
    zip_code = models.CharField(_('Zip Code'),max_length=255,null=True, blank=True)
    street_address = models.CharField(_('Street Address'),max_length=300,null=True, blank=True)

    latitude = models.CharField(_('Latitude'),max_length=255,null=True, blank=True)
    longitude = models.CharField(_('Longitude'),max_length=255,null=True, blank=True)
    contact_number = models.CharField(_('Contact Number'),max_length=255,null=True, blank=True)
    website = models.CharField(_('Website'),max_length=255,null=True, blank=True)

    is_active = models.BooleanField(_('Is Active'),default=0)
    is_verified  = models.BooleanField(default = False)
    
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)


    class Meta:
        ordering = ('name',)
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'


    def save(self, *args, **kwargs):  # new
        if not self.slug or self.name:
            self.slug = slugify(str(self.name))
        return super().save(*args, **kwargs)


    def __str__(self):
        return '{}'.format(self.name)




class Metadata(models.Model):
    shop = models.ForeignKey(Shops, related_name="shop", on_delete=models.CASCADE)
    meta_title = models.CharField(max_length=255,null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    meta_tag = models.CharField(max_length=255,null=True, blank=True)
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        ordering = ('meta_title',)
        verbose_name = 'meta_title'
        verbose_name_plural = 'meta_titles'

    def __str__(self):
        return '{}'.format(self.meta_title)