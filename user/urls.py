from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('account/', views.account),
    path('bookmarks/', views.bookmarks),
    path('cards/', views.cards),
    path('login/', views.login),
    path('notifications/', views.notifications),
    path('pwd_reset/', views.pwd_reset),
]