# Handle the remaining sub URL string

from django.urls import path
from rango import views

app_name = 'rango'

# a list with URLs string
urlpatterns = [
    path('', views.index, name ='index'), # page for index 
    path('about/', views.about, name = 'about') # page for about
]