from django.urls import path
from django.contrib import admin

from . import views

app_name = 'clubs'
urlpatterns = [
    path('', views.index, name='home'),
]