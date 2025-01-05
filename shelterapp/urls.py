from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pet/<str:serial_no>/', views.show_pet_details, name='show_pet_details'),
    path('pet/adopt/<str:serial_no>/', views.adopt_pet, name='adopt_pet'),
    path('wanna_donate/', views.wanna_donate, name='wanna_donate'),
    path('donated_pets/', views.donated_pets, name='donated_pets'),
    path('adopted_pets/', views.adopted_pets, name='adopted_pets'),
    path('authority_view/', views.authority_view, name='authority_view'),
    path('authority_view/all_users', views.all_users, name='all_users'),
    path('authority_view/vet_visit', views.vet_visit, name='vet_visit'),
    
]
