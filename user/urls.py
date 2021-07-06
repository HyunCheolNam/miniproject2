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
    path('logout/', views.logout, name='logout'),

    path('signup/', views.signup, name="signup"),
    path('agreement/', views.agreement, name="agreement"),
    #path('signup_check/',views.signup_check,name="signup_check")
    
    path('find_id/', views.find_id, name="find_id"),
    path('find_pw/', views.find_pw, name="find_pw"),
    path('insert_card/', views.insert_card, name="insert_card"),
    
    #kakaopay
    path('kakao/', views.kakao, name="kakao"),
    path('kakaopay/', views.kakaopay, name="kakaopay"),
    path('approval/', views.approval, name="approval"),
    path('delete_card/', views.delete_card, name="delete_card"),
]