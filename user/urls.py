from django.contrib import admin
from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('account/', views.account, name='account'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('cards/', views.cards, name='cards'),
    path('login/', views.login, name='login'),
    path('notifications/', views.notifications, name='notifications'),
    path('pwd_reset/', views.pwd_reset, name='pwd_reset'),
    path('singup/', views.singup, name="singup"),
]