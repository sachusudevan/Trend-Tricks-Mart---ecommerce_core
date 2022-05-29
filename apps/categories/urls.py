


from django.urls import path
from . import views


app_name = 'categories'

urlpatterns = [
    path('', views.CategoryIndexView.as_view() , name='category.index'),
    path('load_shops_datatable', views.LoadShopsDatatable.as_view(), name='load.category.datatable'),
    path('create/', views.CategoryCreateOrUpdatetView.as_view(), name='category.create'),
    path('<int:id>/update/', views.CategoryCreateOrUpdatetView.as_view(), name='category.update'),
    path('destroy_records/', views.DestroyCategoryRecordsView.as_view(), name='category.recors.destroy'),
]