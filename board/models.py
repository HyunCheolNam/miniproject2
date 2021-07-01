from django.db import models
from user.models import User

# Create your models here.
class Board(models.Model): 
    '''게시판 테이블'''
    '''사용자[1] : 게시글[N] '''
    brd_title = models.CharField(max_length=20, null=True, default='글 제목')
    brd_content = models.TextField(null=True, default='글 내용') # 게시글 NULL 가능
    hash_tags = models.CharField(max_length=100, null=True) # 해시태그 NULL 가능
    brd_hits = models.IntegerField(default=0)
    brd_write_dt = models.DateTimeField()
    # FK 설정 - 사용자
    brd_writer = models.ForeignKey(User, on_delete=models.CASCADE) # 사용자 데이터 삭제 시, 게시글 데이터도 삭제

    class Meta:
        db_table = 'board'

class Comment(models.Model):
    '''댓글 테이블'''
    '''게시글[1] : 댓글[N]'''
    '''댓글[N] : 사용자[1]'''
    cmt_content = models.TextField()
    cmt_write_dt = models.DateTimeField()    
    # FK - 게시글
    board = models.ForeignKey(Board, on_delete=models.CASCADE) # 게시글 삭제 시, 댓글 데이터도 삭제
    # FK - 사용자
    cmt_writer = models.ForeignKey(User, on_delete=models.CASCADE) # 사용자 데이터 삭제 시, 댓글 데이터도 삭제


class FAQ(models.Model):
    '''FAQ 테이블'''
    question = models.TextField()
    answer = models.TextField()
    faq_hits = models.IntegerField(default=0)
    category = models.IntegerField(default=3)
    # class Category(models.IntegerChoices):
    #     '가입/탈퇴' = 0
    #     '사용방법' = 1
    #     '커뮤니티' = 2

    # category = models.IntegerField(choices=Category.choices)

