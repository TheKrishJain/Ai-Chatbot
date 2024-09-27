from django.contrib import admin
from django.urls import path , include
from . import views
from .views import chat_view

urlpatterns = [

    path('', views.index), 
       path('api/chat', chat_view, name='chat_view'),
]# urls.py



