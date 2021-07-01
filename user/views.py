from django.shortcuts import render

def account(request):
    return render(request,'user/account.html')

def bookmarks(request):
    return render(request,'user/bookmarks.html')

def cards(request):
    return render(request,'user/cards.html')

def login(request):
    return render(request,'user/login.html')

def notifications(request):
    return render(request, 'user/notifications.html')

def pwd_reset(request):
    return render(request,'user/pwd_reset.html')