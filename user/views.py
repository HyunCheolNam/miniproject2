from django.http.response import JsonResponse
from board import views as b_views
from django.shortcuts import redirect, render
from django.http import HttpResponse
from user.models import User
from user import kakaoAPI
import qrcode
#해쉬암호화에 사용되는 라이브러리
from argon2 import PasswordHasher
#kakaopay
import requests

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
        #db_data = User.objects.filter(user_id=user_id) 먼저 해서 데이터 가져 온 후         
        # 어렵게 가져오는 데이터 db_data.values('user_pw')[0]['user_pw'] : query에서 원하는 데이터 추출할 때 사용 . 
        try:
            #다른 방법으로 구현해야 할거같다..아마도.. 비밀번호를 암호화해서 넣었기때문에 user_pw를 가져와도 똑같지 않다.
            db_data = User.objects.filter(user_id=user_id)
            db_id = db_data.values('user_id')[0]['user_id']
            db_password = db_data.values('user_pw')[0]['user_pw']
            if PasswordHasher().verify(db_password, user_pw) == True and db_id == user_id:
                user = User.objects.get(user_id = user_id)
            #db_user_id = User.objects.get(user_id=user_id)
            #pw_verify = PasswordHasher.verify()
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
        try:
            user_id = request.POST.get('user_id')
            password =request.POST.get('user_pw') 
            #argon2 라이브러리를 사용해서 해쉬 암호화.
            user_pw = PasswordHasher().hash(password)
            user_name = request.POST.get('user_name')
            user_nick = request.POST.get('user_nick')
            user_email = request.POST.get('user_email')
            user_phone = request.POST.get('user_phone')
            user_address = request.POST.get('sample6_address')

            latlng = address_to_latlng(user_address)
            user_lat = latlng[0]
            user_lng = latlng[1]
            if request.POST.get('phone_alram') == True :
                isPhoneAlert = 1
            else:
                isPhoneAlert = 0
            if request.POST.get('email_alram') == True :
                isEmailAlert = 1
            else:
                isEmailAlert = 0

            user = User(user_id= user_id, user_pw= user_pw, user_name = user_name, user_nick= user_nick, user_email = user_email, user_phone = user_phone, user_address = user_address,user_lat = user_lat, user_lng = user_lng, isPhoneAlert = isPhoneAlert, isEmailAlert = isEmailAlert )
            user.save()

            print(user_id, user_pw,user_name,user_nick,user_email,user_address,user_phone,isPhoneAlert,isEmailAlert, user_lat,user_lng)
            return redirect('user:login')
        except:
            return HttpResponse("회원가입에 실패했습니다.")
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

def find_id(request):
    return render(request, 'user/find_id.html')

def find_pw(request):
    return render(request, 'user/find_pw.html')

def insert_card(request):
    if request.method == 'GET':
        return render(request,'user/insert_card.html', {})
    else:
        #카드정보
        card1 = request.POST.get('card1')
        card2 = request.POST.get('card2')
        card3 = request.POST.get('card3')
        card4 = request.POST.get('card4')
        card_num = card1+'-'+card2+'-'+card3+'-'+card4
        card_pw = request.POST.get('card_pw')
        card_cvc = request.POST.get('card_cvc')
        card_holder = request.POST.get('card_holder')
        validation_date = request.POST.get('validation_date')
        card_info = {
            'card_num' : card_num,
            'card_pw' : card_pw,
            'card_cvc' : card_cvc,
            'card_holder' : card_holder,
            'validation_date' : validation_date
        }
        #데이터 가져올떄 QR코드 생성
        #QR CODE
        card_qr = qrcode.make(card_info)
        card_qr.save("card.jpg")
        
        print(card_num,card_pw,card_cvc,card_holder,validation_date)
        return render(request,'user/cards.html')

    return render(request, 'user/insert_card.html')

def kakao(request):
    return render(request,"user/kakao.html")

def kakaopay(request):
    if request.method == "POST":
        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": "KakaoAK " + "08f51e0e00d6be66ee734ab9f9ec6bea",   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }
        params = {
            "cid": "TC0ONETIME",    # 테스트용 코드
            "partner_order_id": "1001",     # 주문번호
            "partner_user_id": "german",    # 유저 아이디
            "item_name": "연어초밥",        # 구매 물품 이름
            "quantity": "1",                # 구매 물품 수량
            "total_amount": "12000",        # 구매 물품 가격
            "tax_free_amount": "0",         # 구매 물품 비과세
            "approval_url" : "http://127.0.0.1:8000/user/approval",
            "cancel_url": "http://127.0.0.1:8000/board/main",
            "fail_url": "http://127.0.0.1:8000/board/main",
        }

        print("Header :" ,headers)
        print("params :" ,params)
        
        
        res = requests.post(URL, headers=headers, params=params)
        request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
        next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
        return redirect(next_url)
    return render(request, 'user/kakaopay.html')

def approval(request):
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "08f51e0e00d6be66ee734ab9f9ec6bea",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    print("test")
    params = {
        "cid": "TC0ONETIME",    # 테스트용 코드
        "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": "1001",     # 주문번호
        "partner_user_id": "german",    # 유저 아이디
        "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
        "amount": {
            "total": 12000,
            "tax_free": 0,
            "vat": 200,
            "point": 0,
            "discount": 0
            },
    }

    res = requests.post(URL, headers=headers, params=params)
    amount = res.json()['amount']['total']
    res = res.json()
    context = {
        'res': res,
        'amount': amount,
    }
    print(res)
    print(amount)
    return render(request, 'user/approval.html',context)