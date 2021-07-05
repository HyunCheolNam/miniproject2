from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Laundry, Machine, Option
from user import models as user_model
from user import kakaoAPI
from django.shortcuts import get_object_or_404

import pandas as pd
import numpy as np


def laundryDB(request):
    data1 = pd.read_csv("laundry_data.csv", encoding="CP949")
    data2 = pd.read_csv("세탁기 정보.csv", encoding="CP949")
    data3 = pd.read_csv("건조기 정보.csv", encoding="CP949")
    data4 = pd.read_csv("추가요금 정보.csv", encoding="CP949")

    df = data1.iloc[:, :]
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
    for raw in range(len(data1)):
        item = []
        for column in range(len(df.columns)):
            item.append(df_laundry[column][1][raw])

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


def search_map(request):
    
    try:
        user_id = request.session['user_id']
    except:
        return redirect('user:login')
    else:
        RestAPIKey = "e10fc0ca482b5375d98fe727a94ba06b"
        keyword = request.GET['keyword']
        # print(keyword)
        param = keyword + " 셀프빨래방"
        kakao = kakaoAPI.KakaoLocalAPI(RestAPIKey)
        document = kakao.search_keyword_simple(param)
        
        user = user_model.User.objects.get(user_id=user_id)
        user_center = {
            'lat': user.user_lat,
            'lng': user.user_lng
        }
        
        laundry_list = Laundry.objects.order_by('id')
        position = []
        
        if len(document) != 0:

            # print(document)
            for index in range(len(document)):
                x = document[index]["x"]
                y = document[index]["y"]
                place_url = document[index]["place_url"]
                place_name = document[index]["place_name"]
                position.append([x,y,place_name,place_url])
            # print(position)

        pos = {
            'location' : position
        }

        # print(position)
        context = {
            'laundry_list': laundry_list, 
            'user_center': user_center,
            'position': document
            # 'review':review,
            # 'price':price
        }

    return render(request, 'laundry/search_map.html', context)


def detail_page(request, laundry_id):
    # login_session = request.session.get('login_session', '')
    # context = {'login_session':login_session}
    laundry = get_object_or_404(Laundry, id=laundry_id)
    machine = get_object_or_404(Machine, laundry_id=laundry_id)
    option = get_object_or_404(Option, laundry_id=pk)
    # review = get_object_or_404(user_model.Reviews, laundry_id=pk)

    context = {'laundry': laundry}
    # context['machine'] = machine
    # context['option'] = option
    # context['review'] = review

    return render(request, 'laundry/detail_page.html', context)

# class detailList(generic.ListView):
#     return render (request, 'laundry/detail_page.html')


def index(request):
    laundry_list = Laundry.objects.order_by('id')
    context = {'laundry_list': laundry_list}

    return render(request, 'laundry/board_list.html', context)


def detail(request, laundry_id):
    laundry = Laundry.objects.get(id=laundry_id)
    review = user_model.Reviews.objects.filter(laundry_id__contains=laundry_id)
    machine = Machine.objects.filter(laundry_id__contains=laundry_id)

    star_result = 0
    if review.count() != 0:
        for star in review:
            star_result = star_result + star.star

        star_result = star_result / review.count()

    review = {
        "review_num": review.count(),
        "star": star_result
    }

    washer_price, dryer_price = 0, 0
    for m in machine:
        if m.type == "0":
            if washer_price > m.basic_rate:
                washer_price = m.basic_rate
        else:
            if dryer_price > m.basic_rate:
                dryer_price = m.basic_rate

    price = {
        'washer_price': washer_price,
        'dryer_price': dryer_price
    }

    context = {'laundry': laundry, 'review': review, 'price': price}

    return render(request, 'laundry/detail_page.html', context)
