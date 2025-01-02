from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pet/<str:serial_no>/', views.show_pet_details, name='show_pet_details'),
    path('pet/adopt/<str:serial_no>/', views.adopt_pet, name='adopt_pet'),
    
]
