import os
import time
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("__file__"))) + "/speak_image")
import Speak_Image


from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# set default directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# access module library
customModule = Speak_Image.speak_image()

# cuda gpu setting
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="1"

# Create your views here.
def index(request):
    target_list = os.listdir(os.path.dirname(__file__) + '/static/media/target/')

    # Sub PJT3 > Req. 2-1 메인페이지 접속시 voice conversion 대상 목록 파라미터 전달
    # TODO
    # 음성 변환을 위한 wav 파일 목록을 읽어와 파일명 Index.html 내 파라미터로 전달 파라미터로 전달
    context = '{"target_list": ["p225_268","p229_367","p226_215"]}'

    return render(request, 'index.html', context)

# API
@csrf_exempt
def imageCaptioning(request):
    if request.method == 'POST' and request.FILES['file']:

        # Sub PJT2 > Req. 2-1 Image Captioning 비즈니스 로직 정의
        # TODO
        # 이미지 파일 기반으로 image captioning 모듈 호출
        data = ["A man walking a dog on a leash.",
                 "A man and a dog are in the snow.",
                 "A man riding a snowboard down a snow covered slope.",
                 "A person walking a dog on a leash."]

        return JsonResponse({'result': 'OK', 'data': data})
    return JsonResponse({'result': 'ERROR'})

@csrf_exempt
def tts(request):
    sentence = request.POST['sentence']
    if sentence:
        # Sub PJT2 > Req. 2-2 TTS 비즈니스 로직 정의
        # TODO
        # 이미지 파일 기반으로 tts 모듈 호출
        path = '/static/media/src_voice.wav'

        return JsonResponse({'result': 'OK', 'data': path})
    return JsonResponse({'result': 'ERROR'})


@csrf_exempt
def voiceConversion(request):
    type = request.POST['type']
    if type:
        # Sub PJT3 > Req. 2-2 Voice Conversion 비즈니스 로직 정의
        # TODO
        # 이미지 파일 기반으로 voice converseion 모듈 호출
        output_path = '/static/media/src_voice.wav'

        return JsonResponse({'result': 'OK', 'data': output_path})
    return JsonResponse({'result': 'ERROR'})


