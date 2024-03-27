from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list.as_view(), name='menu_list'),
]