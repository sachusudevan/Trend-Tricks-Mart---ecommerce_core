from django.urls import include, path, re_path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'shops'


from apps.product import views as productview



urlpatterns = [
    path('', views.ShopsIndexView.as_view() , name='shops.index'),
    path('load_shops_datatable', views.LoadShopsDatatable.as_view(), name='load.shops.datatable'),
    path('create/', views.ShopsCreateOrUpdatetView.as_view(), name='shops.create'),
    path('<int:id>/update/', views.ShopsCreateOrUpdatetView.as_view(), name='shops.update'),
    path('destroy_records/', views.DestroyStaffRecordsView.as_view(), name='shops.recors.destroy'),

    path('<slug:shop_slug>/', include([

        path('', views.ShopDashboardIndexView.as_view() , name='shops.shop.index'),  
        path('products/', productview.ShopProductsIndexView.as_view() , name='shops.shop.product.index'),  

        path('manufacturers/', include([
            path('', productview.ShopManufacturesIndexView.as_view() , name='shops.shop.manufacture.index'),  
            path('load_shops_manufactur_datatable', productview.LoadShopManufacturesDatatable.as_view() , name='load.shop.manufactur.datatable'),  
            path('create/', productview.ShopManufacturesCreateOrUpdatetView.as_view() , name='shops.shop.manufactur.create'),  
            path('<int:id>/update/', productview.ShopManufacturesCreateOrUpdatetView.as_view() , name='shops.shop.manufactur.update'),  
            path('destroy_records/', productview.ShopManufacturesDestroyRecordsView.as_view() , name='shops.shop.manufacture.destroy'),  

        ])),
    ])),


    # path('<slug:shop_slug>/', views.ShopDashboardIndexView.as_view() , name='shops.shop.index'),  
    



]