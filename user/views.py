from board import views as b_views
from django.shortcuts import redirect, render
from django.http import HttpResponse
from user import models as user_model
import json

def account(request):
    return render(request,'user/account.html')

def bookmarks(request):
    return render(request,'user/bookmarks.html')

def cards(request):
    return render(request,'user/cards.html')

def login(request):
    ## GET 방식일 때 그냥 화면
    if request.method == 'GET':
        return render(request,'user/login.html', {})
    ## POST 방식일 때 
    else:
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        try:
            user = user_model.User.objects.get(user_id = user_id, user_pw = user_pw)
            request.session['user_nick'] = user.user_nick
            request.session['user_id'] = user.user_id
        except:
            # return render(request,'user/login.html', {안내메시지})
            return HttpResponse('로그인 실패')
        else:
            return redirect(b_views.main)

def notifications(request):
    return render(request, 'user/notifications.html')

def pwd_reset(request):
    return render(request,'user/pwd_reset.html')

