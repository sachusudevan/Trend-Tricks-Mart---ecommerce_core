


from django.urls import path
from . import views


app_name = 'groups'

urlpatterns = [
     path('', views.GroupsIndexView.as_view() , name='groups.index'),
     path('load_shops_datatable', views.LoadShopsDatatable.as_view(), name='load.groups.datatable'),
     path('create/', views.GroupsCreateOrUpdatetView.as_view(), name='groups.create'),
     path('<int:id>/update/', views.GroupsCreateOrUpdatetView.as_view(), name='groups.update'),
     path('destroy_records/', views.DestroyGroupRecordsView.as_view(), name='groups.recors.destroy'),
]