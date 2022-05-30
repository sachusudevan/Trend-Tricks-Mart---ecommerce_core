from random import random
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import Users
from apps.categories.models import Categories
from apps.groups.models import Groups
from django.utils.text import slugify




def manufacture_cover_image(self,fileame):
    return f"manufactures/cover/{self.id}/{self.name}-{random()}.png"

def manufacture_cover_default_image():
    return f"default/default-manufacture-image.jpg"

def manufacture_logo_image(self,fileame):
    return f"manufactures/logo/{self.id}/{self.name}-{random()}.png"

def manufacture_logo_default_image():
    return f"default/default-manufacture-logo.png"





class Manufactures(models.Model):
    name = models.CharField(_('Name'),max_length=255,null=True, blank=True)
    slug = models.SlugField(_('Slug'), unique=True, editable=False)
    description = models.TextField(_('Description') , null=True, blank=True)
    logo = models.ImageField(_('Logo'), upload_to=manufacture_logo_image, default=manufacture_logo_default_image, null=True, blank=True)
    cover_image = models.ImageField(_('Cover Image'), upload_to=manufacture_cover_image, default=manufacture_cover_default_image, null=True, blank=True)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    website = models.CharField(_('Website'),max_length=255,null=True, blank=True)
    is_active = models.BooleanField(_('Is Active'),default=0)
    
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Manufacture'
        verbose_name_plural = 'Manufactures'

    def save(self, *args, **kwargs):  # new
        if not self.slug or self.name:
            self.slug = slugify(str(self.name))
        return super().save(*args, **kwargs)


    def __str__(self):
        return '{}'.format(self.name)





def products_thumbnail_image(self,):
    return f"products/thumbnail/{self.name}-{random()}.png"

def products_thumbnail_default_image():
    return f"default/default-product-thumbnail.png"





class Products(models.Model):

    name = models.CharField(_('Name'),max_length=255,null=True, blank=True)
    description = models.TextField(_('Description') , null=True, blank=True)
    thumbnail = models.ImageField(_('Thumbnail'), upload_to=products_thumbnail_image, default=products_thumbnail_default_image, null=True, blank=True)
    slug = models.SlugField(_('Slug'), unique=True, editable=False)

    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    manufacture = models.ForeignKey(Manufactures, on_delete=models.CASCADE)
    
    price = models.FloatField(_('Price'), null=True, blank=True)
    discount_type = models.IntegerField(_('Discount Type'), null=True, blank=True) 
    discount = models.IntegerField(_('Discount'), null=True, blank=True) 
    discounted_price = models.FloatField(_('Discounted Price'), null=True, blank=True)

    sku = models.CharField(_('SKU'),max_length=100,null=True, blank=True)
    #product barcode unique number. 
    barcode = models.CharField(_('Barcode'), unique=True, max_length=255,null=True, blank=True)
    quantity = models.IntegerField(_('Quantity'), null=True, blank=True)

    #Allow customers to purchase products that are out of stock.
    is_backorders  = models.BooleanField(_('IsBackorders'), null=True, blank=True)

    #et if the product is a physical or digital item. Physical products may require shipping.
    is_physical = models.BooleanField(_('IsPhysical'), null=True, blank=True)

    weight = models.CharField(_('Weight'), max_length=255,null=True, blank=True)
    width = models.IntegerField(_('Width'), null=True, blank=True)
    height = models.IntegerField(_('Height'), null=True, blank=True)
    length = models.IntegerField(_('Length'), null=True, blank=True)


    status = models.IntegerField(_('Status'), null=True, blank=True) 
    publishing_date = models.DateTimeField(_('Publishing Date'), null=True, blank=True)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)

    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)



    class Meta:
        ordering = ('id',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        # abstract = True


    def save(self, *args, **kwargs):  # new
        if not self.slug or self.name:
            self.slug = slugify(str(self.name))
        return super().save(*args, **kwargs)


    def __str__(self):
        return '{}'.format(self.name)