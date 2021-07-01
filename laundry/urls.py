from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.index),
    path('search_map/', views.search_map),
    path('detail_page/', views.detail_page),
]