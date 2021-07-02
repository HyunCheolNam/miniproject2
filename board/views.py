from django.shortcuts import render

def board(request):
    return render(request,'board/board.html')

def main(request):
    return render(request, 'main.html')

def qna(request):
    return render(request, 'board/qna.html')

def board_write(request):
    return render(request, 'board/board_write.html')

def board_see(request):
    return render(request , 'board/board_see.html')

def board_modify(request):
    return render(request, 'board/board_modify.html')