from random import random
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import Users
from apps.categories.models import Categories
from apps.groups.models import Groups
from django.utils.text import slugify
from multiselectfield import MultiSelectField



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
    IDEAL_FOR_CHOICES =(
        ("Men", "Men"),
        ("Women", "Women"),
        ("Boys", "Boys"),
        ("4", "Four"),
        ("5", "Five"),
    )
    name = models.CharField(_('Name'),max_length=255,null=True, blank=True)
    description = models.TextField(_('Description') , null=True, blank=True)
    thumbnail = models.ImageField(_('Thumbnail'), upload_to=products_thumbnail_image, default=products_thumbnail_default_image, null=True, blank=True)
    slug = models.SlugField(_('Slug'), unique=True, editable=False)

    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    manufacture = models.ForeignKey(Manufactures, on_delete=models.CASCADE)
    
    price = models.FloatField(_('Price'), null=True, blank=True)
   

    sku = models.CharField(_('SKU'),max_length=100,null=True, blank=True)
    barcode = models.CharField(_('Barcode'), unique=True, max_length=255,null=True, blank=True)
    quantity = models.IntegerField(_('Quantity'), null=True, blank=True)

    ideal_for = models.CharField(max_length=50, null=True, blank=True)

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




class Metadata(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    meta_title = models.CharField(max_length=255,null=True, blank=True)
    meta_name = models.CharField(max_length=255,null=True, blank=True)
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




class Discount(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(_('Name'),max_length=255,null=True, blank=True)
    description = models.TextField(_('Description') , null=True, blank=True)
    discount_type = models.IntegerField(_('Discount Type'), null=True, blank=True) 
    discount = models.FloatField(_('Discount'), null=True, blank=True) 
    discounted_price = models.FloatField(_('Discounted Price'), null=True, blank=True)
    is_active = models.BooleanField(_('Is Active'), null=True, blank=True) 
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)
    class Meta:
        ordering = ('id',)
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'
        # abstract = True

    def __str__(self):
        return '{}'.format(self.name)




class ProductColor(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(_('Name'),max_length=255,null=True, blank=True)
    color_code = models.CharField(_('Color Code'), max_length=100,null=True, blank=True)
    is_active = models.BooleanField(_('Is Active'), null=True, blank=True) 
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        ordering = ('id',)
        verbose_name = 'ProductColor'
        verbose_name_plural = 'ProductColors'
        # abstract = True


    def __str__(self):
        return '{}'.format(self.name)



class ProductSize(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(_('Name'),max_length=255,null=True, blank=True)
    size = models.CharField(_('Size'), max_length=100,null=True, blank=True)
    is_active = models.BooleanField(_('Is Active'), null=True, blank=True) 
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        ordering = ('id',)
        verbose_name = 'ProductSize'
        verbose_name_plural = 'ProductSizes'
        # abstract = True

    def __str__(self):
        return '{}'.format(self.name)


