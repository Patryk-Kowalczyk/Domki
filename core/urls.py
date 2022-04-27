from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('o-nas/', views.about, name='o-nas'),
    path('co-robimy/', views.whatmedo, name='co-robimy'),
    path('realizacje/', views.realizations, name='realizacje'),
    path('kontakt/', views.contact, name='kontakt'),
    path('domek/<slug:slug>', views.cottage, name='cottage'),
]
