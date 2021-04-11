from IC.image_captioning import Caption_Model
from TTS.tacotron import TTS_Model
from VC.voice_conversion import VC_Model
from KOR.kor_tts import KOR_Model
import cv2

from django.conf import settings

import os
import sys
import json
import urllib.request

# client_id = "t6TKlUbfHk2gsyHQKcYt" # 개발자센터에서 발급받은 Client ID 값
# client_secret = "K5mC720BS1" # 개발자센터에서 발급받은 Client Secret 값

class speak_image():
    def __init__(self):

        #initialize models
        self.caption_model = Caption_Model()
        self.tts_model = TTS_Model()        
        self.vc_model = VC_Model()
        self.kor_model = KOR_Model()

    # 이미지 불러오기
    def load_image(self, img_url):
        
        # img = cv2.imread(img_url, cv2.IMREAD_COLOR)
        result = self.caption_model.inference(img_url)
        # cv2.imshow("image", img)
        
        # tts_model.inference("text", tts_output_path)
        output_tts_path = self.tts_model.inference(result[0], "/home/ubuntu/s04p23a402/backend/media/"+ result[0][:10] + ".wav")
        
        # vc_model.inference(원본 음성파일 경로, 바꿀 음성 파일 경로, 저장 경로)

        output_vc_path = self.vc_model.inference("/home/ubuntu/s04p23a402/backend/media/" + result[0][:10] + ".wav", "/home/ubuntu/test/backend/Codes/speak_image/VC/song0.wav", "/home/ubuntu/s04p23a402/backend/media/vc_"+ result[0][:10] + ".wav")
        
        encText = urllib.parse.quote(result[0])
        data = "source=en&target=ko&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        response_body = response.read()
        koText = response_body.decode('utf-8')
        koDict = json.loads(koText)
        
        
        output_kor_path = self.kor_model.inference(koDict['message']['result']['translatedText'] , "/home/ubuntu/s04p23a402/backend/media/")
        
        print(output_kor_path)
        return result, output_tts_path, output_vc_path, output_kor_path
    # 이미지로 부터 캡션 생성    
    def caption_image(self):
        pass
        # sub-pjt 1 명세서를 다시 보고 이미지 캡셔닝. -> Import 하는 방식으로 sub1 이미지 캡션 (Inference 함수 호출)
        # 얘를 구현하기.

    # 한가지 캡션 선택
    def select_caption(self):
        pass
    # 선택한 캡션 음성으로 변환
    def text_to_speech(self,output_path):
        pass 
    def convert_voice(self,src_path, tar_voice_path, output_path):
        pass

    @property
    def img_path(self):
        return self.__img_path
    
    @img_path.setter
    def img_path(self, img_path):
        self.__img_path = img_path

    @property
    def captions_list(self):
        return self.__captions_list
