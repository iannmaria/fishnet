from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.fisherman_registration, name='fisherman_registration'),
    path('dashboard/', views.fisherman_dashboard, name='fisherman_dashboard'),
    path('add/', views.add_catch, name='add_catch'),
    path('complaint/', views.file_complaint, name='file_complaint'),
]
