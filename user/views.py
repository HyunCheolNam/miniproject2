from django.http.response import JsonResponse
from board import views as b_views
from django.shortcuts import redirect, render
from django.http import HttpResponse
from user.models import User
from user import kakaoAPI

def account(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id = user_id)
    return render(request,'user/account.html', {'user': user})

## 마이페이지 수정 - 비밀번호 
def change_pw(request):
    user_id = request.session['user_id']

    previous_pw = request.POST['previous_pw']
    new_pw = request.POST['new_pw']
    check_pw = request.POST['check_pw']

    user = User.objects.get(user_id=user_id)

    if user.user_pw == previous_pw:
        result = {'previous': 'True' }
    else:
        result = {'previous': 'False'}
        return JsonResponse({'result': result})
    
    if new_pw == check_pw:
        result['new'] = 'True'
        user.user_pw = new_pw
        user.save('user:account')
    else:
        result['new'] = 'False'
        
    return JsonResponse({'result': result})

## 마이페이지 수정 - 닉네임
def change_nick(request):
    user_id = request.session['user_id']
    new_nick = request.POST['new_nick']

    user = User.objects.get(user_id=user_id)

    user.user_nick = new_nick
    user.save()

    return render(request, 'user/account.html', {'user': user})

### 마이페이시 수정 - 주소
def change_address(request):
    user_id = request.session['user_id']
    new_address = request.POST['new_address']

    user = User.objects.get(user_id=user_id)
    new_lat, new_lng = address_to_latlng(new_address)

    user.user_address = new_address
    user.user_lat = new_lat
    user.user_lng = new_lng

    user.save()

    return render(request, 'user/account.html', {'user': user})

### 마이페이지 수정 - 이메일 주소
def change_email(request):
    user_id = request.session['user_id']
    new_email = request.POST['new_email']

    user = User.objects.get(user_id=user_id)

    user.user_email = new_email
    user.save()

    return render(request, 'user/account.html', {'user': user})

### 마이페이지 수정 - 휴대폰 번호
def change_phone(request):
    user_id = request.session['user_id']
    new_phone = request.POST['new_phone']

    user = User.objects.get(user_id=user_id)

    user.user_phone = new_phone
    user.save()

    return render(request, 'user/account.html', {'user': user})



def bookmarks(request):
    return render(request,'user/bookmarks.html')

def cards(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id = user_id)

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
            user = User.objects.get(user_id = user_id, user_pw = user_pw)
            request.session['user_nick'] = user.user_nick
            request.session['user_id'] = user.user_id            
        except:
            # return render(request,'user/login.html', {안내메시지})
            return HttpResponse('로그인 실패')
        else:
            return redirect(b_views.main)

def logout(request):
    request.session.clear()
    return redirect('board:main')


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


### 주소 -> 위도 경도 변환
def address_to_latlng(query):
    RestAPIKey = "e10fc0ca482b5375d98fe727a94ba06b"
    kakao = kakaoAPI.KakaoLocalAPI(RestAPIKey)
    address = kakao.search_address(query)
    (lat, lng) = (address[0]['y'], address[0]['x'])

    return (lat, lng)