from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('dzialki-nad-jeziorem', views.plots, name='dzialki-nad-jeziorem'),
    path('domek/<slug:slug>', views.cottage, name='cottage'),
]
