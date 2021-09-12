from django.urls import path
from . import views

app_name = 'ajax'
urlpatterns = [
    path('', views.index, name='index'),
    path('ajax-number/', views.ajax_number, name='ajax_number'), #ajax_numberは、views.pyで宣言した関数名
]