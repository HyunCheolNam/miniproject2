from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from user.models import User
from laundry.models import Laundry
from board.models import Board
from django.http import JsonResponse
from django.forms.models import model_to_dict
from datetime import datetime
from django.core.paginator import Paginator

# 게시판 목록
def board(request):
    page = request.GET.get('page')
    if not page:
        page = 1

    board_list = Board.objects.order_by('-id')
    
    p = Paginator(board_list, 10)

    pages = p.page(page)

    start_page = (int(page) - 1) // 10 * 10 + 1
    end_page = start_page + 9

    if end_page > p.num_pages:
        end_page = p.num_pages
    
    context = {
        'board_list' : pages,
        'pagination' : range(start_page, end_page+1)
    }

    return render(request,'board/board.html', context)

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

# 게시판 글쓰기 
def board_write(request):
    try:
        user_id = request.session['user_id']
        user = user = User.objects.get(user_id=user_id)
    except:
        return HttpResponse('잘못된 접근')
    else:
        return render(request, 'board/board_write.html')

def board_write_data(request):
    user_id = request.session['user_id']
    user = user = User.objects.get(user_id=user_id)

    brd_title = request.POST['brd_title']
    brd_content = request.POST['brd_content']
    brd_tags = request.POST['brd_tags']

    brd_write_dt = datetime.now()
    try:
        board = Board(brd_title=brd_title, brd_content=brd_content, hash_tags=brd_tags, brd_hits=0,
            brd_write_dt=brd_write_dt, brd_writer_id = user.id)
        board.save()
    except:
        result = False
    else:
        result = True
    
    return JsonResponse({'result': result})


def detail(request, board_id):
    board = Board.objects.get(id=board_id)
    board.brd_hits += 1 # 조회수 증가
    board.save()

    return render(request , 'board/detail.html', {'board':board})

def delete_board(request):
    board_id = request.POST['board_id']
    
    try:
        board = Board.objects.get(id=board_id)
        board.delete()
    except:
        result = False
    else:
        result = True
    
    return JsonResponse({'result': result})

def modify_board(request, board_id):
    board = Board.objects.get(id=board_id)
   
    return render(request, 'board/board_modify.html', {'board':board})

def board_modify_data(request):
    
    board_id = request.POST['board_id']
    brd_title = request.POST['brd_title']
    brd_content = request.POST['brd_content']
    brd_tags = request.POST['brd_tags']
    
    try:
        board = Board.objects.get(id=board_id)        
    except:
        result = False
    else:
        board.brd_title = brd_title
        board.brd_content = brd_content
        board.hash_tags = brd_tags
        board.save()

        result = True
    
    return JsonResponse({'result': result})
