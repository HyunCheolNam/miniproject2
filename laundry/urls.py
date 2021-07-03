from django.contrib import admin
from django.urls import path
from . import views

app_name = 'laundry'
urlpatterns = [
    path('laundryDB/', views.laundryDB, name = 'laundryDB'),
    path('search_map/', views.search_map, name='search_map'),
    path('detail_page/', views.detail_page, name='detail_page'),
]