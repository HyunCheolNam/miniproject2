from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from user.models import User
from laundry.models import Laundry
from board.models import Board, Comment, FAQ
from django.http import JsonResponse
from django.forms.models import model_to_dict
from datetime import datetime
from django.core.paginator import Paginator
import smtplib
from email.mime.text import MIMEText

# 메인페이지
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

# 게시판 목록
def board(request):
    page = request.GET.get('page')
    if not page:
        page = 1

    keyword = request.GET.get('keyword')
    if not keyword:
        keyword = ''
    
    # if request.method == 'GET':
    board_list = Board.objects.filter(hash_tags__contains=keyword).order_by('-id')
    p = Paginator(board_list, 10)
    pages = p.page(page)

    start_page = (int(page) - 1) // 10 * 10 + 1
    end_page = start_page + 9

    if end_page > p.num_pages:
        end_page = p.num_pages
    
    context = {
        'board_list' : pages,
        'keyword': keyword,
        'pagination' : range(start_page, end_page+1)
    }
    return render(request,'board/board.html', context)

# 게시판 글쓰기 (AJAX 데이터용)
def board_write(request):
    try:
        user_id = request.session['user_id']
        user = User.objects.get(user_id=user_id)
    except:
        return HttpResponse('잘못된 접근')
    else:
        return render(request, 'board/board_write.html')

### 게시판 글쓰기 (AJAX 데이터용)
def board_write_data(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)

    brd_title = request.POST.get('brd_title')
    brd_content = request.POST.get('brd_content')
    brd_tags = request.POST.get('brd_tags')

    try:
        board = Board(brd_title=brd_title, brd_content=brd_content, hash_tags=brd_tags, brd_hits=0, brd_write_dt=datetime.now(), brd_writer = user)
        board.save()
    except:
        result = False
    else:
        result = True
    
    return JsonResponse({'result': result})

### 게시글 보기
def detail(request, board_id):
    board = Board.objects.get(id=board_id)
    board.brd_hits += 1 # 조회수 증가
    board.save()

    return render(request , 'board/detail.html', {'board':board})

### 댓글 달기
def comment_create(request, board_id):
    print('here')
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)

    board = get_object_or_404(Board, pk=board_id)
    board.comment_set.create(
        cmt_content = request.POST.get('content'), 
        cmt_write_dt = datetime.now(),
        cmt_writer = user
    )

    return redirect('board:detail', board_id=board.id)

### 댓글 달기 (AJAX 데이터용)
def comment_delete(request):
    cmt_id = request.POST.get('cmt_id')
    try:
        cmt = Comment.objects.get(id=cmt_id)
        cmt.delete()
    except:
        result = False
    else:
        result = True
    return JsonResponse({'result': result})

### 게시판 삭제 
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

### 게시판 수정
def modify_board(request, board_id):
    board = Board.objects.get(id=board_id)
   
    return render(request, 'board/board_modify.html', {'board':board})

### 게시판 수정 (AJAX 데이터용)
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

### FAQ / Q&A 화면
def qna(request):
    page = request.GET.get('page')

    if not page:
        page = 1

    faqs = FAQ.objects.all()

    p = Paginator(faqs, 5)
    pages = p.page(page)

    start_page = (int(page) - 1) // 5 * 5 + 1
    end_page = start_page + 4

    if end_page > p.num_pages:
        end_page = p.num_pages
    
    context = {
        'faq_list' : pages,
        'pagination' : range(start_page, end_page+1)
    }

    return render(request, 'board/qna.html', context)

### 메일 보내기
def send_mail(from_email, to_email, msg):
    APP_PW = 'hcxrlccpcltibqep'
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465) # SMTP 설정
    smtp.login(from_email, APP_PW) # 인증정보 설정
    msg = MIMEText(msg)
    msg['Subject'] = '[문의사항]    ' + to_email # 제목
    msg['To'] = from_email # 수신 이메일
    smtp.sendmail(from_email, from_email, msg.as_string())
    smtp.quit()

### Q&A 메일 처리
def contact(request):
    ADMIN_MAIL = 'kokoritaaa7@gmail.com'
    if request.method == 'POST':
        email = request.POST.get('email')
        comment = request.POST.get('qna_content')
        # 발신자주소, 수신자주소, 메시지
        send_mail(ADMIN_MAIL, email, comment)
        return JsonResponse({'result':True})
    return redirect('board:qna')
