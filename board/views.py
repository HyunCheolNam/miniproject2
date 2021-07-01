from django.shortcuts import render

def board(request):
    return render(request,'board/board.html')

def main(request):
    return render(request, 'main.html')

def qna(request):
    return render(request, 'board/qna.html')

def board_write(request):
    return render(request, 'board/board_write.html')