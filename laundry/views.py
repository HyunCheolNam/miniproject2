from django.shortcuts import render
from .models import Laundry,Machine,Option

import pandas as pd
import numpy as np

def laundryDB(request):
    data1 = pd.read_csv("laundry_data.csv", encoding="CP949")
    data2 = pd.read_csv("세탁기 정보.csv", encoding="CP949")
    data3 = pd.read_csv("건조기 정보.csv", encoding="CP949")
    data4 = pd.read_csv("추가요금 정보.csv", encoding="CP949")

    df = data1.iloc[:, :-1]
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
        Laundry(laundry_name=item[0], laundry_address=item[1], laundry_road=item[2],laundry_lng=item[3],
        laundry_lat=item[4],laundry_tel=item[5],laundry_img=item[6], washer_cnt=item[7],dryer_cnt=item[8]).save()
    
    # 세탁기 정보 저장
    for raw in range(len(data2)):
        item = []
        for column in range(len(data2.columns)):
            item.append(df_washer[column][1][raw])

        L_id = Laundry.objects.get(id=item[0])
        Machine(laundry=L_id, useable=item[1], machine_category=item[2], machine_type=item[3],basic_rate=item[4]).save()
    
    # 건조기 정보 저장
    for raw in range(len(data3)):
        item = []
        for column in range(len(data3.columns)):
            item.append(df_dryer[column][1][raw])

        L_id = Laundry.objects.get(id=item[0])
        Machine(laundry=L_id, useable=item[1], machine_category=item[2], machine_type=item[3],basic_rate=item[4]).save()

    # 추가요금/옵션 정보 저장
    for raw in range(len(data4)):
        item = []
        for column in range(len(data4.columns)):
            item.append(df_option[column][1][raw])

        L_id = Laundry.objects.get(id=item[0])
        Option(laundry=L_id, option_name=item[1], add_fee=item[2]).save()

    return render(request,'laundry/laundryDB.html')

def search_map(request):
    return render(request,'laundry/search_map.html')

def detail_page(request):
    return render (request, 'laundry/detail_page.html')