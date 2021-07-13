from django import db
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from user.models import Payment, User
from user import kakaoAPI
import qrcode
#해쉬암호화에 사용되는 라이브러리
from argon2 import PasswordHasher

#kakaopay
import requests
## Mail
import smtplib
from email.mime.text import MIMEText

import datetime as dt
from random import * 

## 마이페이지 첫 화면
def account(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id = user_id)
    return render(request,'user/account.html', {'user': user})

## 마이페이지 수정 - 비밀번호 
def change_pw(request):
    user_id = request.session['user_id']
   
    db_data = User.objects.get(user_id=user_id)
    previous_pw = request.POST['previous_pw']
    new_pw = request.POST['new_pw']

    try:
        PasswordHasher().verify(db_data.user_pw, previous_pw)
        db_data.user_pw = PasswordHasher().hash(new_pw)
        db_data.save()
        result = {'previous': True }
        if db_data.isTempPW:
            db_data.isTempPW = False
    except:
        result = {'previous': False}

    return JsonResponse(result)

## 마이페이지 수정 - 닉네임
def change_nick(request):
    user_id = request.session['user_id']
    new_nick = request.POST['new_nick']

    user = User.objects.get(user_id=user_id)

    user.user_nick = new_nick
    user.save()

    request.session['user_nick'] = user.user_nick

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

### 마이페이지 즐겨찾기 - 미완
def bookmarks(request):
    return render(request,'user/bookmarks.html')

### 마이페이지 결제수단
def cards(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id = user_id)
    card_info = Payment.objects.filter(users=user)
    card_infos = {
        'card_info' : card_info
    }
    path = "static/img/qrcode/"

    for card in card_info:
        cards = {'card_num' : card.card_num, 
        'card_pw' : card.card_pw,
        'card_cvc' : card.card_cvc,
        'card_holder' : card.card_holder,
        'validate_dt' : card.validate_dt }
        
        card_qr = qrcode.make(cards)
        card_qr.save(path+f"{card.card_holder}{card.users_id}.jpg")
    # for i in range(len(card_info)):
    #     secret_number = randint(0,9999)
    #     card = [secret_number]
        
    #     #내일부터 하면 된다 카드데이터 저장해서 딕셔너리로 전달하고 html에 뿌리기
    #     #QR코드 생성해서 화면에 표시하기
    #     #del버튼 누르면 카드 db에서 제거하기.
    #     print(card_info)
    return render(request,'user/cards.html',card_infos)

### 로그인
def login(request):
    ## GET 방식일 때 그냥 화면
    if request.method == 'GET':
        return render(request,'user/login.html', {})
    ## POST 방식일 때 
    else:
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        #db_data = User.objects.filter(user_id=user_id) 먼저 해서 데이터 가져 온 후         
        # 어렵게 가져오는 데이터 :db_data.values('user_pw')[0]['user_pw'] : query에서 원하는 데이터 추출할 때 사용 . 
        try:
            #다른 방법으로 구현해야 할거같다..아마도.. 비밀번호를 암호화해서 넣었기때문에 user_pw를 가져와도 똑같지 않다.
            db_data = User.objects.get(user_id=user_id)
            db_id = db_data.user_id
            db_password = db_data.user_pw
            print(db_data.isTempPW)
            # db_data = User.objects.filter(user_id=user_id)
            # db_id = db_data.values('user_id')[0]['user_id']
            # db_password = db_data.values('user_pw')[0]['user_pw']
            if PasswordHasher().verify(db_password, user_pw) == True and db_id == user_id:
                # user = User.objects.get(user_id = user_id)
                request.session['user_nick'] = db_data.user_nick
                request.session['user_id'] = db_data.user_id
        except:
            return JsonResponse({'result':False})   
        else:
            if db_data.isTempPW:
                return JsonResponse({'result':'temp'})

            return JsonResponse({'result':True})

### 로그아웃
def logout(request):
    request.session.clear()
    return redirect('board:main')

### 회원가입
def signup(request):
    if request.session['agreement']:
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
                return render(request,'user/login.html')
            except:
                return HttpResponse("회원가입에 실패했습니다.")
    else:
        # 일단 그냥 다시 agreement 페이지로
        pass
    #return redirect('user:login')

### 개인정보동의서
def agreement(request):
    if request.POST.get('agreement1', False) and request.POST.get('agreement2', False):
            request.session['agreement'] = True
            return redirect('user:signup')
    else:
        request.session['agreement'] = False
        return render(request, 'user/agreement.html')

### 주소 -> 위도 경도 변환
def address_to_latlng(query):
    RestAPIKey = "e10fc0ca482b5375d98fe727a94ba06b"
    kakao = kakaoAPI.KakaoLocalAPI(RestAPIKey)
    address = kakao.search_address(query)
    (lat, lng) = (address[0]['y'], address[0]['x'])

    return (lat, lng)

### 아이디 찾기
def find_id(request):
    FLAG = 'ID'
    if request.method == 'GET':
        return render(request, 'user/find_id.html')
    else:
        email = request.POST.get('email')
        try:
            user = User.objects.get(user_email=email)
            user_id = user.user_id
        except:
            result = False
        else:
            sendMail_for_find(email, user_id, FLAG)
            result = True
        return JsonResponse({'result':result})

### 아이디 / 임시비밀번호 이메일 전송  
def sendMail_for_find(to_email, info, flag):
    APP_PW = 'hcxrlccpcltibqep'
    from_email = 'kokoritaaa7@gmail.com' # ADMIN_MAIL
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465) # SMTP 설정
    smtp.login(from_email, APP_PW) # 인증정보 설정
    if flag == 'ID':
        msg = '고객님의 아이디는 ' + info + '입니다.'

        msg = MIMEText(msg)
        msg['Subject'] = '[아이디 찾기]    FLAUNDRY 에서 조회하신 아이디입니다.' # 제목
    else:
        msg = '고객님의 임시 비밀번호는 ' + info + '입니다 \
             \n로그인 후 마이페이지에서 비밀번호를 변경해주세요.'

        msg = MIMEText(msg)
        msg['Subject'] = '[비밀번호 찾기]    FLAUNDRY 에서 발급된 임시 비밀번호입니다.'
            # 제목

    msg['To'] = to_email # 수신 이메일
    smtp.sendmail(from_email, to_email, msg.as_string())
    smtp.quit()

### 비밀번호 찾기
def find_pw(request):
    FLAG = 'PW'
    tempPW = makeTempPw()
    print(tempPW)
    if request.method == 'GET':
        return render(request, 'user/find_pw.html')
    else:
        user_id = request.POST.get('user_id')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        try:
            user = User.objects.get(user_id=user_id,user_email=email,user_phone=phone)
            user.user_pw = PasswordHasher().hash(tempPW)
            user.isTempPW = True
            user.save()
        except:
            result = False
        else:
            sendMail_for_find(email, tempPW, FLAG)
            result = True
        return JsonResponse({'result':result})

### 임시 비밀번호 생성 
def makeTempPw():
    import string
    import random

    _LENGTH = 8

    # 숫자 + 대소문자
    string_pool = string.ascii_letters + string.digits

    # 랜덤한 문자열 생성
    tempPW = ""
    for i in range(_LENGTH):
        tempPW += random.choice(string_pool)
        
    return tempPW

### 카드입력
def insert_card(request):
    if request.method == 'GET':
        return render(request,'user/insert_card.html', {})
    else:
        user_id = request.session.get('user_id')
        user = User.objects.get(user_id= user_id)
        #카드정보
        card1 = request.POST.get('card1')
        card2 = request.POST.get('card2')
        card3 = request.POST.get('card3')
        card4 = request.POST.get('card4')
        card_pw = request.POST.get('card_pw')
        card_cvc = request.POST.get('card_cvc')
        card_holder_lastname = request.POST.get('card_holder_lastname')
        card_holder_firstname = request.POST.get('card_holder_firstname')
        validation_date = request.POST.get('validation_date')

        card_num = card1+'-'+card2+'-'+card3+'-'+card4
        card_holder_lastname = card_holder_lastname.upper() # 첫글자 대문자로 만들어주는 코드
        card_holder_firstname = card_holder_firstname.upper()
        card_holder = card_holder_firstname + ' ' + card_holder_lastname # 나중에 UI에 표시하기 편하게 성과 이름을 . 로 구분
        # card_info = {
        #     'card_num' : PasswordHasher().hash(card_num),
        #     'card_pw' : PasswordHasher().hash(card_pw),
        #     'card_cvc' : PasswordHasher().hash(card_cvc),
        #     'card_holder' : card_holder,
        #     'validation_date' : validation_date
        # }
        validation_date = dt.datetime.strptime(validation_date,"%Y-%m").date() #str를 날짜로 변환
        
        #데이터 가져올떄 QR코드 생성
        #QR CODE
        # card_qr = qrcode.make(card_info)
        # card_qr.save("card.jpg")
        card = Payment(card_num = PasswordHasher().hash(card_num), card_pw = PasswordHasher().hash(card_pw), card_cvc = PasswordHasher().hash(card_cvc), card_holder = card_holder, validate_dt = validation_date,users=user)
        card.save()

        #print(card_num,card_pw,card_cvc,card_holder,validation_date)
        return redirect('user:cards')
        #return render(request, 'user/insert_card.html')

### 카드삭제
def delete_card(request):
    pk = request.POST.get('pk')
    
    user_id = request.session['user_id']
    user = User.objects.get(user_id = user_id)
    card_info = Payment.objects.get(id=pk)
    card_info.delete()
    card = Payment.objects.all()
    print(card)

    #return redirect('user:cards')
    # return render(request, 'user:cards', {})
    return JsonResponse({'result' : True})

### 카카오페이
def kakao(request):
    return render(request,"user/kakao.html")

### 카카오페이 결제창
def kakaopay(request):
    if request.method == "POST":
        total_cost = request.POST.get('total_score')
        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": "KakaoAK " + "08f51e0e00d6be66ee734ab9f9ec6bea",   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }
        params = {
            "cid": "TC0ONETIME",    # 테스트용 코드
            "partner_order_id": "1001",     # 주문번호
            "partner_user_id": "FLAUNDRY",    # 유저 아이디
            "item_name": "세탁",        # 구매 물품 이름
            "quantity": "1",                # 구매 물품 수량
            "total_amount": total_cost,        # 구매 물품 가격
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

### 카카오페이 승인창
def approval(request):
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "08f51e0e00d6be66ee734ab9f9ec6bea",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",    # 테스트용 코드
        "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": "1001",     # 주문번호
        "partner_user_id": "FLAUNDRY",    # 유저 아이디
        "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
    }
    res = requests.post(URL, headers=headers, params=params)
    print(res)
    

    amount = res.json()["amount"]["total"]
    res = res.json()
    context = {
        'res': res,
        'amount': amount,
    }
    return render(request, 'user/approval.html',context)
