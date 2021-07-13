from django.db import models
from laundry.models import Laundry

# Create your models here.
class User(models.Model):
    '''사용자 테이블'''
    user_id = models.CharField(max_length=20, unique=True) # ID
    user_pw = models.CharField(max_length=20) # PW
    user_name = models.CharField(max_length=20) # 이름 - ERD에 없는데 추가함
    user_nick = models.CharField(max_length=20) # 닉네임
    user_email = models.EmailField(max_length=254, unique=True) # 이메일
    user_phone = models.CharField(max_length=20,unique=True)
    user_address = models.TextField() # 사용자 주소
    user_lat = models.FloatField(null=True) # 사용자 위도 주소
    user_lng = models.FloatField(null=True) # 사용자 경도 주소
    isEmailAlert = models.BooleanField(default=True) # 알림 기본값 True
    isPhoneAlert = models.BooleanField(default=True) # 알림 기본값 True
    isTempPW = models.BooleanField(default=False) # 임시비밀번호발급 여부 기본값 False

    class Meta:
        db_table = 'user'

class Payment(models.Model):
    '''결제수단 테이블'''
    ''' 사용자[1] : 결제수단[N] '''
    card_num = models.CharField(max_length=20) # 카드 번호
    validate_dt = models.DateField() # 카드 유효기간
    card_holder = models.CharField(max_length=20) 
    card_pw = models.CharField(max_length=20) # 카드 비밀번호
    card_cvc = models.CharField(max_length=5)
    # FK 설정 - 사용자
    users = models.ForeignKey(User, on_delete=models.CASCADE) # 사용자 데이터 삭제 시, 결제 수단 데이터도 삭제

class Bookmark(models.Model): 
    '''즐겨찾기 테이블'''
    ''' 사용자[1] : 즐겨찾기[N] '''
    ''' 즐겨찾기[1] : 세탁소 [1] '''
    # FK 설정 - 사용자
    users = models.ForeignKey(User, on_delete=models.CASCADE) # 사용자 데이터 삭제 시, 북마크 데이터도 삭제
    # FK 설정 - 세탁소
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE) # 세탁소 데이터 삭제 시, 북마크 데이터 삭제 

class Reviews(models.Model):
    '''리뷰 테이블'''
    star = models.FloatField(default=0.0)
    review_content = models.TextField()
    review_data = models.DateField()
    # FK - 사용자
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    # FK - 세탁소
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE)