from django.shortcuts import render
from user.models import User
from laundry.models import Laundry
from django.http import JsonResponse
from django.forms.models import model_to_dict

def board(request):
    return render(request,'board/board.html')

def main(request):
    user = User.objects.get(user_name="박지혜")
    user_center = {
        'lat' : user.user_lat,
        'lng' : user.user_lng
    }
    ### TEST
    # print(user_center.user_lat)
    # print(user_center.user_lng)
    # print(user_center)
    
    return render(request, 'main.html', {'user_center': user_center})

# main에서 세탁소 정보 마커용 
def marker_data(request):
    # markers = Laundry.objects.all()
    markers = User.objects.all() # 세탁소 데이터 없어서 일단 user로 테스트
    # markers = User.objects.filter(id=3)
    marker_list = []
    for d in markers:
        d = model_to_dict(d)
        marker_list.append(d)
    return JsonResponse(marker_list, safe=False)


def qna(request):
    return render(request, 'board/qna.html')