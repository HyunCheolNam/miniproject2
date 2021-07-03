from django.contrib import admin
from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('account/', views.account, name='account'),

    path('change_pw/', views.change_pw, name='change_pw'),
    path('change_nick/', views.change_nick, name='change_nick'),
    path('change_address/', views.change_address, name='change_address'),
    path('change_email/', views.change_email, name='change_email'),
    path('change_phone/', views.change_phone, name='change_phone'),

    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('cards/', views.cards, name='cards'),
    path('login/', views.login, name='login'),
    path('notifications/', views.notifications, name='notifications'),
    path('pwd_reset/', views.pwd_reset, name='pwd_reset'),
    path('singup/', views.singup, name="singup"),
]