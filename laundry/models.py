from django.db import models

# Create your models here.
class Laundry(models.Model):
    '''세탁소 테이블'''
    laundry_name = models.CharField(max_length=30) # 세탁소 이름
    laundry_address = models.TextField() # 세탁소 지번 주소
    laundry_road = models.TextField() # 세탁소 도로명 주소
    laundry_lat = models.FloatField() # 세탁소 위도
    laundry_lng = models.FloatField() # 세탁소 경도
    laundry_tel = models.TextField() # 세탁소 전화번호
    laundry_img = models.CharField(max_length=100) # 세탁소 이미지
    laundry_page = models.TextField() # 세탁소 카카오맵 페이지 번호
    washer_cnt = models.IntegerField() # 세탁기 개수
    dryer_cnt = models.IntegerField() # 건조기 개수

    class Meta:
        db_table = "laundry"

class Machine(models.Model):
    '''세탁기와 건조기 테이블'''
    useable = models.BooleanField()
    machine_category = models.IntegerField()
    machine_type = models.IntegerField()
    basic_rate = models.IntegerField()
    # 세탁소 FK
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE)

class Option(models.Model):
    '''추가 옵션 테이블'''
    option_name = models.CharField(max_length=100)
    add_fee = models.IntegerField()
    # 세탁소 FK
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE)

