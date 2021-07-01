from django.shortcuts import render

def index(request):
    return render(request,'base.html')

def search_map(request):
    return render(request,'laundry/search_map.html')

def detail_page(request):
    return render (request, 'laundry/detail_page.html')