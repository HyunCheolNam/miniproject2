from django.shortcuts import render

import pandas as pd
import numpy as np

def laundryDB(request):
    data = pd.read_csv("landry_data.csv")

    data_landry = data.iloc[:, [3,4,6,11,12,13,14]]

    list_landry = []

    for j in range(len(data_landry)):
        list_landry.append(list(data_landry.loc[j]))

    

    return render(request,'laundry/laundryDB.html')

def search_map(request):
    return render(request,'laundry/search_map.html')

def detail_page(request):
    return render (request, 'laundry/detail_page.html')