from django.urls import path, re_path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login', views.LoginView.as_view(), name= 'login'),
    re_path(r'^signout', views.signout, name='signout'),
]
