from django.urls import path, include
from . import views

app_name = 'files'

urlpatterns = [
        path('', views.index, name='index'),
        path('new_file', views.new_file, name='new_file'), 
        #記述後に,views.pyにアップロードの処理を記述
]