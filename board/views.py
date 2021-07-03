from django.shortcuts import render
from user.models import User
from laundry.models import Laundry
from django.http import JsonResponse
from django.forms.models import model_to_dict

def board(request):
    return render(request,'board/board.html')

def main(request):

    try:
        user_id = request.session['user_id']
    ### 로그인 전 -> 강의장 위치로 출력
    except: 
        user_center = {
            'lat' : 37.480885919228776,
            'lng' : 126.8821083975363
        }
    else:
        user = User.objects.get(user_id=user_id)
        user_center = {
        'lat' : user.user_lat,
        'lng' : user.user_lng
    }
    
    return render(request, 'main.html', {'user_center': user_center})

# main에서 세탁소 정보 마커용 
def marker_data(request):
    markers = Laundry.objects.all()
    # markers = User.objects.all() # 세탁소 데이터 없어서 일단 user로 테스트
    # markers = User.objects.filter(id=3)
    marker_list = []
    for d in markers:
        d = model_to_dict(d)
        marker_list.append(d)
    return JsonResponse(marker_list, safe=False)


def qna(request):
    return render(request, 'board/qna.html')

def board_write(request):
    return render(request, 'board/board_write.html')

def board_see(request):
    return render(request , 'board/board_see.html')

def board_modify(request):
    return render(request, 'board/board_modify.html')