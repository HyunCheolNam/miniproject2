from django.db.models.aggregates import Sum
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.forms.models import model_to_dict

from .models import Laundry, Machine, Option
from user.models import Reviews
from user import models as user_model
from user import kakaoAPI
from django.shortcuts import get_object_or_404

import pandas as pd
import numpy as np
import math
from haversine import haversine
from django.db.models import Q, Count, Avg


def laundryDB(request): 
    data1 = pd.read_csv("laundry_data.csv", encoding="CP949")
    data2 = pd.read_csv("세탁기 정보.csv", encoding="CP949")
    data3 = pd.read_csv("건조기 정보.csv", encoding="CP949")
    data4 = pd.read_csv("추가요금 정보.csv", encoding="CP949")

    df = data1.iloc[:,:]
    df_laundry = []
    df_washer = []
    df_dryer = []
    df_option = []

    # 데이터프레임 한 행씩 저장
    for items in df.iteritems():
        df_laundry.append(items)

    for items in data2.iteritems():
        df_washer.append(items)

    for items in data3.iteritems():
        df_dryer.append(items)

    for items in data4.iteritems():
        df_option.append(items)

    # name - 크린토피아 코인워시 독립문현대점, [column][1][raw]
    # print(df_laundry[0][1][0])

    # 세탁소 정보 저장
    for raw in range(len(df)):
        item = []
        for column in range(len(df.columns)):
            item.append(df_laundry[column][1][raw])
            # print(item)
        
        #### 수집 시 lat, lng 순서가 바뀌어 있어서 laundry_lng=item[3],laundry_lat=item[4] 로 수정
        Laundry(laundry_name=item[0], laundry_address=item[1], laundry_road=item[2], laundry_lng=item[3],
        laundry_lat=item[4], laundry_tel=item[5], laundry_img=item[6], washer_cnt=item[7], dryer_cnt=item[8], laundry_page=item[9]).save()

    # 세탁기 정보 저장
    for raw in range(len(data2)):
        item = []
        for column in range(len(data2.columns)):
            item.append(df_washer[column][1][raw])

        L_id = Laundry.objects.get(id=item[0])
        Machine(laundry=L_id, useable=item[1], machine_category=item[2],
                machine_type=item[3], basic_rate=item[4]).save()

    # 건조기 정보 저장
    for raw in range(len(data3)):
        item = []
        for column in range(len(data3.columns)):
            item.append(df_dryer[column][1][raw])

        L_id = Laundry.objects.get(id=item[0])
        Machine(laundry=L_id, useable=item[1], machine_category=item[2],
                machine_type=item[3], basic_rate=item[4]).save()

    # 추가요금/옵션 정보 저장
    for raw in range(len(data4)):
        item = []
        for column in range(len(data4.columns)):
            item.append(df_option[column][1][raw])

        L_id = Laundry.objects.get(id=item[0])
        Option(laundry=L_id, option_name=item[1], add_fee=item[2]).save()

    return render(request, 'laundry/laundryDB.html')

# DB 조회를 이용한 검색
def search_map(request):
    
    try:
        user_id = request.session['user_id']
        keyword = request.GET.get('keyword1', "")
        check_list = request.POST.getlist('sel[]')
        # print("check_list: ", check_list)
        # 검색어
        # keyword = request.GET['keyword']
        # keyword = request.GET.get('keyword','')
    except:
        return redirect('user:login')
    else:

        # 0. 데이터 준비 : DB에서 데이터 가져오기
        user = user_model.User.objects.get(user_id=user_id)
        user_center = {
                'lat': user.user_lat,
                'lng': user.user_lng
        }
        laundry_list = Laundry.objects.order_by('id')
        machine_list = Machine.objects.values('laundry','machine_category', 'machine_type','basic_rate').order_by('laundry','machine_category','machine_type')
        machine_list = machine_list.distinct()
        review_list = Reviews.objects.values('laundry').annotate(Sum('star'),Count('star'))   # 별점 총 합, 총 갯수
       
        # washer_list = Machine.objects.filter(machine_category=0).values('laundry','machine_type').annotate(Count('machine_type'))
        # dryer_list = Machine.objects.filter(machine_category=1).values('laundry','machine_type')
        

        #####       왼쪽 사이드바       #####
        if len(check_list) != 0:
            for check in check_list:
                if check:
                    machine_list = machine_list.filter(
                        Q(machine_type__icontains=check)
                    )
        

        #####       오른쪽 사이드바     #####
        # 사용자로부터 입력 받은 keyword에 대하여,
        # 1. 입력 : 카카오 API에 parameter 값 -> 출력 : document, list
        
        # DB 조회
        if keyword :
            laundry_list = laundry_list.filter(
                Q(laundry_name__icontains=keyword) |
                Q(laundry_address__icontains=keyword) |
                Q(laundry_road__icontains=keyword) |
                Q(laundry_lat__icontains=keyword) |
                Q(laundry_lng__icontains=keyword) |
                Q(laundry_tel__icontains=keyword) |
                Q(washer_cnt__icontains=keyword) |
                Q(dryer_cnt__icontains=keyword)

            ).distinct()

        # DB 정보와 거리를 비교하여 가장 가까운 코인세탁소 찾기
        if laundry_list.count() != 0:
            min, i = 1000, 0
            start = (float(user.user_lat), float(user.user_lng))
            for laundry in laundry_list:
                goal=(float(laundry.laundry_lat), float(laundry.laundry_lng))
                km = haversine(start, goal)
                # print(laundry.laundry_name, " : ", km, "km")
                if min > km :
                    min = km
                    i = laundry.id

            result_laundry = laundry_list.get(id=i)
            user_center['lat'] = result_laundry.laundry_lat
            user_center['lng'] = result_laundry.laundry_lng


            # print(position)
            context = {
                'laundry_list': laundry_list,
                'user_center': user_center,
                'keyword': keyword,
                'name' : result_laundry.laundry_name,
                'review_list' : review_list,
                'machine_list': machine_list
            }
        else : 
            context = {
                'laundry_list': laundry_list,
                'user_center': user_center,
                'name' : user.user_nick,
                'review_list' : review_list,
                'machine_list': machine_list
            }


    return render(request, 'laundry/search_map.html', context)


# KakaoAPI를 이용한 검색
def search_map2(request):
    
    try:
        user_id = request.session['user_id']
        # keyword = request.GET['keyword']
        param = request.GET.get("keyword2","")
    except:
        return redirect('user:login')
    else:
        # 사용자로부터 입력 받은 keyword에 대하여,
        # 1. 입력 : 카카오 API에 parameter 값 -> 출력 : document, list
        user = user_model.User.objects.get(user_id=user_id)
        user_center = {
            'lat': user.user_lat,
            'lng': user.user_lng
        }
        name = ''
        machine_list = Machine.objects.values('laundry','machine_category', 'machine_type','basic_rate').order_by('laundry','machine_category','machine_type')
        machine_list = machine_list.distinct()
        review_list = Reviews.objects.values('laundry').annotate(Sum('star'),Count('star'))   # 별점 총 합, 총 갯수
        

        RestAPIKey = "e10fc0ca482b5375d98fe727a94ba06b"
        kakao = kakaoAPI.KakaoLocalAPI(RestAPIKey)

        
        if param != "":
            document = kakao.search_keyword_radius(param, user.user_lat, user.user_lng, 100)
            
            # 2. 유효한 입력 값인지 확인 : 주소가 있는지 없는지 확인
            if len(document) != 0 :
            # 3. True : 키워드 주소를 기준으로 DB조회 -> 사용자 위치를 기반으로 해당 DB내용 지도에 출력

                start = (float(user.user_lat), float(user.user_lng))
                min, i = 1000, 0
                for index, d in enumerate(document):
                    goal=(float(d['y']), float(d['x']))
                    km = haversine(start, goal)
                    # print(d['place_name'], " : ", km, "km")
                    if min > km :
                        min = km
                        i = index

                
                # print(min, "Km!")
                # print(document[i]['place_name'])

                user_center['lat'] = document[i]['y']
                user_center['lng'] = document[i]['x']
                name = document[i]['place_name']
                param = document[i]['address_name']
                param = param[:7]
                print("param: ", param)
                
                # print("키워드 좌표", user_center['lat'], user_center['lng'])
        
                # DB 조회
                laundry_list = Laundry.objects.order_by('id')
                if param :
                    laundry_list = laundry_list.filter(
                        Q(laundry_name__icontains=param) |
                        Q(laundry_address__icontains=param) |
                        Q(laundry_road__icontains=param) |
                        Q(laundry_lat__icontains=param) |
                        Q(laundry_lng__icontains=param) |
                        Q(laundry_tel__icontains=param) |
                        Q(washer_cnt__icontains=param) |
                        Q(dryer_cnt__icontains=param)

                    ).distinct()


                context = {
                    'laundry_list': laundry_list,
                    'user_center': user_center,
                    'name' : name,
                    'review_list':review_list,
                    'machine_list': machine_list
                }

    return render(request, 'laundry/search_map.html', context)


def detail_page(request, laundry_id):
    # login_session = request.session.get('login_session', '')
    # context = {'login_session':login_session}
    laundry = get_object_or_404(Laundry, id=laundry_id)
    
    # 리뷰 조회
    review_list = Reviews.objects.filter(laundry=laundry_id)
    machine_list = Machine.objects.filter(laundry=laundry_id)
    option_list = Option.objects.filter(laundry=laundry_id)

    # 세탁기, 건조기 최저 가격 찾기
    d_min, w_min = 10000, 10000
    for machin in machine_list:
        # print(machin)
        if machin.machine_category == 0:
            if machin.basic_rate < d_min:
                d_min = machin.basic_rate
        else:
            if machin.basic_rate < w_min:
                w_min = machin.basic_rate

    star = 0
    if review_list.count() !=0:
        for review in review_list:
            star = star + review.star
        star = star / review_list.count()
        # print(star)
    else:
        star = 0

    review_num = review_list.count()

    context = {
        'laundry': laundry,
        'review': review_list,
        'machine' : machine_list,
        'option' : option_list,
        'W_price' : w_min,
        'D_price' : d_min,
        'star' : star,
        'review_num' : review_num
    }
   

    return render(request, 'laundry/detail_page.html', context)

def select(request):
    pass


# 지도, 반경 ~Km내의 세탁소 거리계산 함수
def distance(lat1, lng1, lat2, lng2) :
    theta = lng1 - lng2
    dist1 = math.sin(deg2rad(lat1)) * math.sin(deg2rad(lat2))
    dist2 = math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2))
    dist2 = dist2* math.cos(deg2rad(theta))
    dist = dist1 + dist2
    dist = math.acos(dist)
    dist = rad2deg(dist) * 60 * 1.1515 * 1.609344
    return dist

def deg2rad(deg):
    return deg * math.pi / 180.0

def rad2deg(rad):
    return rad * 180.0 / math.pi

def map_data(request):
    data = Laundry.objects.all()
    
    keyword = request.GET['keyword']
    # print(keyword)
    param = keyword
    RestAPIKey = "e10fc0ca482b5375d98fe727a94ba06b"
    kakao = kakaoAPI.KakaoLocalAPI(RestAPIKey)
    document = kakao.search_keyword_simple(param)

    lat = document[0]["x"]
    lng = document[0]["y"]
    place_url = document[0]["place_url"]
    place_name = document[0]["place_name"]

    map_list = []

    for d in data:
        d = model_to_dict(d) # QuerySet -> Dict
        dist = distance(float(lat), float(lng), d['laundry_lat'], d['laundry_lng'])
    
        if(dist <= 10): # 10km 이내의 장소만 응답결과로 저장
            map_list.append(d)
    
    # dict가 아닌 자료는 항상 safe=False 옵션 사용
    return JsonResponse(map_list, safe=False)


