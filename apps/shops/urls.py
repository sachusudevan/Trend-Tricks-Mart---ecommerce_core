from django.urls import include, path, re_path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'shops'





urlpatterns = [
    path('', views.ShopsIndexView.as_view() , name='shops.index'),
    path('load_shops_datatable', views.LoadShopsDatatable.as_view(), name='load.shops.datatable'),
    path('create/', views.ShopsCreateOrUpdatetView.as_view(), name='shops.create'),
    path('<int:id>/update/', views.ShopsCreateOrUpdatetView.as_view(), name='shops.update'),
    path('destroy_records/', views.DestroyStaffRecordsView.as_view(), name='shops.recors.destroy'),

    # path('<slug:shop_slug>/', include([

    #     path('', views.ShopDashboardIndexView.as_view() , name='shops.shop.index'),  

    # ])),


    path('<slug:shop_slug>/', views.ShopDashboardIndexView.as_view() , name='shops.shop.index'),  
    path('<slug:shop_slug>/products/', views.ShopDashboardIndexView.as_view() , name='shops.shop.product.index'),  



]