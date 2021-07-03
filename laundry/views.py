from django.shortcuts import render
from .models import Laundry

import pandas as pd
import numpy as np

def laundryDB(request):
    data = pd.read_csv("laundry_data.csv", encoding="CP949")

    df = data.iloc[:, :-1]
    df_laundry = []

    for items in df.iteritems():
        df_laundry.append(items)

    print(df_laundry[0][1][0]) # name - 크린토피아 코인워시 독립문현대점, [column][1][raw]

    for raw in range(len(df)):
        item = []
        for column in range(len(df.columns)):
            item.append(df_laundry[column][1][raw])
        
        #### 수집 시 lat, lng 순서가 바뀌어 있어서 laundry_lng=item[3],laundry_lat=item[4] 로 수정
        Laundry(laundry_name=item[0], laundry_address=item[1], laundry_road=item[2],laundry_lng=item[3],
        laundry_lat=item[4],laundry_tel=item[5],laundry_img=item[6], washer_cnt=item[7],dryer_cnt=item[8]).save()

    return render(request,'laundry/laundryDB.html')

def search_map(request):
    return render(request,'laundry/search_map.html')

def detail_page(request):
    return render (request, 'laundry/detail_page.html')