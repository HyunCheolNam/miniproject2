from board import views as b_views
from django.shortcuts import redirect, render
from django.http import HttpResponse
from user import models as user_model
import json

def account(request):
    if request.method == 'GET':
        user_id = request.session['user_id']
        user = user_model.User.objects.get(user_id = user_id)
        return render(request,'user/account.html', {'user': user})
    else: # 수정을 위한 데이터 전송        
        # 아직 개발 못함
        pass

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


def signup(request):
    if request.method == 'GET':
        return render(request,'user/signup.html', {})
    else:
        return render(request,'user/login.html')
    
    #return redirect('user:login')

def signup_check(request):
    
    return redirect('user:login')
