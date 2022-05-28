from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'shops'

urlpatterns = [
    path('', views.ShopsIndexView.as_view() , name='shops.index'),
    path('load_shops_datatable', views.LoadShopsDatatable.as_view(), name='load.shops.datatable'),
    path('create/', views.ShopsCreateOrUpdatetView.as_view(), name='shops.create'),
    path('<int:id>/update/', views.ShopsCreateOrUpdatetView.as_view(), name='shops.update'),
    path('destroy_records/', views.DestroyStaffRecordsView.as_view(), name='shops.recors.destroy'),
]