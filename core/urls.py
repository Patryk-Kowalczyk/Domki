from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('kontakt/', views.contact, name='contact'),
    path('dzialki-nad-jeziorem/', views.plots, name='dzialki-nad-jeziorem'),
    path('domek/<slug:slug>', views.cottage, name='cottage'),
]
