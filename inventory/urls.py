from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('detail/<int:fish_id>/', views.fish_detail, name='fish_detail'),
]
