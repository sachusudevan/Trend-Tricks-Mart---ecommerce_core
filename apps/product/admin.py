from django.contrib import admin

from apps.product.models import Discount, Manufactures, Metadata, ProductColor, ProductSize, Products


# Register your models here.

admin.site.empty_value_display = ''
class ManufactureAdmin(admin.ModelAdmin):
    model = Manufactures
    list_display = [ 'name','slug','logo','website','is_active','group_id','owner_id']
    list_display_links = ['name']
    search_fields = ('name',)
    list_filter = ('group_id', 'is_active','owner_id',)

    def group_id(self, obj):
            return obj.name

    def owner_id(self, obj):
            return obj.name

admin.site.register(Manufactures,ManufactureAdmin)




class ProductsAdmin(admin.ModelAdmin):
    model = Products
    list_display = ['name','thumbnail','price','quantity','publishing_date','category','group','manufacture','owner']
    list_display_links = ['name']
    search_fields = ('name', 'price','quantity','publishing_date',)
    ordering = ('name',)
    list_filter = ('publishing_date', 'category','group','owner',)

admin.site.register(Products,ProductsAdmin)




class ProductMetadataAdmin(admin.ModelAdmin):
    model = Metadata
    
    list_display = ['meta_title', 'product','meta_description','meta_tag','created_date','modified_date']
    list_display_links = ['meta_title']
    search_fields = ('product','meta_title','meta_tag',)
    fields = ( 'product', ('meta_title', 'meta_description','meta_tag'))
    
    

admin.site.register(Metadata,ProductMetadataAdmin)



class ProductDiscountAdmin(admin.ModelAdmin):
    model = Discount
    list_display = ['name', 'product','description','discount_type','discount','discounted_price','is_active']
    list_display_links = ['name']
    search_fields = ('product','name','discount_type','is_active',)
    list_filter = ('discount_type','discount','discounted_price','is_active',)

admin.site.register(Discount,ProductDiscountAdmin)



class ProductColorAdmin(admin.ModelAdmin):
    model = ProductColor
    list_display = ['name', 'product','color_code','is_active']
    list_display_links = ['name']
    search_fields = ('product','name','color_code','is_active',)
    list_filter = ('color_code','is_active',)


admin.site.register(ProductColor,ProductColorAdmin)



class ProductSizeAdmin(admin.ModelAdmin):
    model = ProductSize
    list_display = ['name', 'product','size','is_active']
    list_display_links = ['name']
    search_fields = ('product','name','size','is_active',)
    list_filter = ('size','is_active',)


admin.site.register(ProductSize,ProductSizeAdmin)