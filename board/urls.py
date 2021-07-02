from django.contrib import admin
from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('', views.board, name="board"),
    path('main/', views.main, name='main'),
    path('qna/', views.qna, name="qna"),
    path('board_write/', views.board_write, name="board_write"),
    path('board_see/', views.board_see, name="board_see"),
]