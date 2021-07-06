import json, requests

class KakaoLocalAPI:
    
    #-- REST API, header, URL --#
    def __init__(self, APIkey):
        # REST API키 초기화 및 header 정보 초기화
        self._mykey = APIkey
        self._header = {"Authorization":"KakaoAK {}".format(self._mykey)}
        
        ## kakao local API URL - json
        
        # 1. 주소 검색
        self._URL_1 = "https://dapi.kakao.com/v2/local/search/address.json?"
        # 2. 좌표로 행정구역정보 받기
        self._URL_2 = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?"
        # 3. 좌표로 주소 변환하기
        self._URL_3 = "https://dapi.kakao.com/v2/local/geo/coord2address.json?"
        # 4. 좌표계 반환
        self._URL_4 = "https://dapi.kakao.com/v2/local/geo/transcoord.json?"
        # 5. 키워드로 장소 검색
        self._URL_5 = "https://dapi.kakao.com/v2/local/search/keyword.json?"
        # 6. 카테고리로 장소 검색
        self._URL_6 = "https://dapi.kakao.com/v2/local/search/category.json?"
        
        
    #-- 1. 주소 검색 --#
    def search_address(self, query):
        param = {'query':f"{query}"}
        
        response = requests.get(self._URL_1, params = param, headers = self._header)
        # document = response.json()['documents']
        
        return response.json()['documents']
    
    
    #-- 2. 좌표로 행정구역정보 받기 --#
    def geo_coord2regioncode(self,x,y):
        param = {'x':f"{x}", 'y':f"{y}"}
        
        response = requests.get(self._URL_2, params = param, headers = self._header)
        document = response.json()['documents']
        
        return document
    
    
    #--3. 좌표로 주소 변환하기 --#
    def geo_coord2address(self,x,y,input_coord):
        param = {'x':f"{x}", 'y':f"{y}", 'input_coord':f"{input_coord}"}
        
        response = requests.get(self._URL_3, params = param, headers = self._header)
        document = response.json()['documents']
        
        return document
    
    
    #--4. 좌표계 변환 --#
    def geo_transcoord(self,x,y,input_coord, output_coord):
        param = {'x':f"{x}", 'y':f"{y}", 'input_coord':f"{input_coord}", 'output_coord':f"{output_coord}"}
        
        response = requests.get(self._URL_4, params = param, headers = self._header)
        document = response.json()['documents']
        
        return document
    
    
    #--5. 키워드로 장소 검색1 --#
    def search_keyword_simple(self, query):
        param = {'query':f"{query}"}
        
        response = requests.get(self._URL_5, params = param, headers = self._header)
        document = response.json()['documents']
        
        return document
    
    #--5. 키워드로 장소 검색2 --#
    def search_keyword_radius(self, query, x, y, radius):
        param = {'query':f"{query}", 'x':f"{x}", 'y':f"{y}", 'radius':f"{radius}"}
        
        response = requests.get(self._URL_5, params = param, headers = self._header)
        document = response.json()['documents']
        
        return document
    
    #--6. 카테고리로 장소 검색 --#
    def search_category(self, cgroup, x, y, radius):
        param = {'category_group_code':f"{cgroup}", 'x':f"{x}", 'y':f"{y}", 'radius':f"{radius}"}
        
        response = requests.get(self._URL_5, params = param, headers = self._header)
        document = response.json()['documents']
        
        return document
    
        
