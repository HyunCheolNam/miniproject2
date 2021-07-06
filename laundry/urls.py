from django.contrib import admin
from django.urls import path
from . import views

app_name = 'laundry'
urlpatterns = [
    path('laundryDB/', views.laundryDB, name = 'laundryDB'),
    path('search_map/', views.search_map, name='search_map'),
    path('search_map2/', views.search_map2, name='search_map2'),
    path('detail_page/<int:laundry_id>', views.detail_page, name='detail_page'),
    # path('index/', views.index, name ='index'),
    # path('<int:laundry_id>/', views.detail, name='detail'),
]