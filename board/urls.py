from django.contrib import admin
from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('', views.board, name="board"),
    path('main/', views.main, name='main'),
    path('qna/', views.qna, name="qna"),
    path('board_write/', views.board_write, name="board_write"),
    path('board_write_data/', views.board_write_data, name="board_write_data"),

    path('<int:board_id>/', views.detail, name='detail'),
    path('comment_create/<int:board_id>/', views.comment_create, name='comment_create'),
    path('comment_delete/', views.comment_delete, name='comment_delete'),

    path('delete_board/', views.delete_board, name='delete_board'),
    path('modify_board/<int:board_id>/', views.modify_board, name='modify_board'),
    path('board_modify_data/', views.board_modify_data, name="board_modify_data"),

    path('contact/', views.contact, name="contact")
]