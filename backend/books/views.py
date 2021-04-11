from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, VoicePattern
from ari.settings import MEDIA_ROOT
from django.views.decorators.http import require_GET, require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from .forms import VoicePatternForm
from .models import Book, Image, Voice
from urllib.request import urlopen
###########

# 이미지 저장

# AI 삽입
import sys; import os
import json
# import cv2
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname("__file__")))))+
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))+
"/Codes/speak_image")
import Speak_Image

# access module library
customModule = Speak_Image.speak_image()


from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# set default directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
  
# access module library
# customModule = Speak_Image.speak_image()

# cuda gup setting
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="1"
from django.views.decorators.csrf import csrf_exempt
# 안드로이드
from django.core.files.storage import FileSystemStorage
# Imaginary function to handle an uploaded file.
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@require_GET
def index(request):
  # target_list = os.listdir(os.path.dirname(__file__) + '/static/media/target/')
  ## TODO
  # 음성 변환을 위한 wav 파일 목록을 읽어와 Index.html 내 파라미터로 전달.
  ## Temp Variable
  # context = {"target_list": ["p225_268", "p229_367", "p226_215"]}

  if not request.user.is_authenticated:
    return render(request, 'accounts/login.html')

  return render(request, 'books/index.html')

# 1. 책 촬영
@require_http_methods(['GET', 'POST'])
@csrf_exempt
def shot_mode(request):
  # if request.method == "POST":
  #   fs = FileSystemStorage()
  #   file = request.FILES['files']
  #   filename = fs.save(file.name, file)
  #   uploaded_file_url = fs.url(filename)

  #   print("여기 아래에 파일이 표시됩니다~~~~~~~~~~~~~~~~!!!!")
  #   print(request.FILES)
  #   return render(request, 'books/shot_mode.html')
  return render(request, 'books/shot_mode.html')

# 2. 음성 녹음
@csrf_exempt
# @require_http_methods(['GET', 'POST'])
def record(request):
  if request.method == 'POST':
    fs = FileSystemStorage()
    file = request.FILES['files']
    filename = fs.save(file.name, file)
    uploaded_file_url = fs.url(filename)

    form = VoicePattern.objects.create(
      speaker_name = request.POST['speaker_name'],
      voice_pattern_url = uploaded_file_url,
      voice_user_id = get_object_or_404(get_user_model(), username = request.POST['speaker_name']).pk,
    )
    print(form)

    return redirect('books:record')
  voice_patterns = VoicePattern.objects.filter(speaker_name=request.user.username)
  context = {
    'voice_patterns': voice_patterns,
  }
  return render(request, 'books/record.html', context)  # 수정

def recordResult(request):
  return render(request, 'books/record_success.html') 

# books/views.py

def library(request):
  books = Book.objects.filter(creator=request.user.username)    # 여기 변경
  context = {
    'books': books
  }
  return render(request, 'books/library.html', context)

def library_mybook(request, pk):
  book = get_object_or_404(Book, pk=pk)
  context = {
    'book': book,
  }
  return render(request, 'books/library_mybook.html', context)

def library_all(reqeust):
  books = Book.objects.all()
  context = {
    'books' : books,
  }
  
  return render(reqeust, 'books/library_all.html', context)

# 4. 놀이터
def playground(request):
  return render(request, 'books/playground.html')


@require_http_methods(['GET', 'POST'])
def mode(request):
  user = request.user
  user.mode = not user.mode
  user.save()
  return redirect('books:index')

# def upload(request):
#     customHeader = request.META['HTTP_MYCUSTOMHEADER']
 
#     # obviously handle correct naming of the file and place it somewhere like media/uploads/
#     uploadedFile = open("recording.ogg", "wb")
#     # the actual file is in request.body
#     uploadedFile.write(request.body)
#     uploadedFile.close()
#     # put additional logic like creating a model instance or something like this here
#     return HttpResponse(escape(repr(request)))

#API
@csrf_exempt
def imageCaptioning(request):
  if request.method == 'POST' and request.FILES['file_id']:
  # if request.method == 'POST':
    booktitle = request.POST['myBooks']
    img = request.FILES['file_id']
    # img를 save 해서 path를 구함
    fs = FileSystemStorage()
    filename = fs.save(img.name, img)
    uploaded_file_url = fs.url(filename)
    # print(uploaded_file_url)
    
    caption_content, tts_path, vc_path, kr_tts_path = customModule.load_image(uploaded_file_url)
    # print("성공: ", caption_content, tts_path, vc_path)
    
    ### DB에 저장처리
    form_book = Book.objects.create(
      title = booktitle,
      thumbnail_url = img,
      creator = request.user.username,
    )
    
    form_img = Image.objects.create(
      caption = caption_content[0],
      book = get_object_or_404(Book, pk=form_book.pk),
      img_url = img
    )
    
    form_voice = Voice.objects.create(
      voice_url = tts_path[31:],
      book = get_object_or_404(Book, pk=form_book.pk),
    )
    
    context = {
      'form_img': form_img,
      'form_book': form_book,
      'form_voice': form_voice,
      'tts_path': tts_path[31:],
      'vc_path': vc_path[31:],
      'kr_tts_path': kr_tts_path[31:],
    }      

    return render(request, 'books/shot.html', context)
  return render(request, 'books/shot_mode.html')

@csrf_exempt
def imageCaptioningAndroid(request):
  # print("여기가 리퀘스트:", request.POST, request.FILES)
  if request.method == 'POST' and request.FILES['files']:
  # if request.method == 'POST':
    booktitle = request.POST['myBooks']
    img = request.FILES['files']
    
    # img를 save 해서 path를 구함
    fs = FileSystemStorage()
    filename = fs.save(img.name, img)
    uploaded_file_url = fs.url(filename)
    # print("경로: ", uploaded_file_url)
    
    caption_content, tts_path, vc_path, kr_tts_path = customModule.load_image(uploaded_file_url)
    # print("성공: ", caption_content, tts_path, vc_path)
    # print(booktitle +"," + filename)
    # print("경로 : " + img)
    
    ### DB에 저장처리
    form_book = Book.objects.create(
      title = booktitle,
      thumbnail_url = uploaded_file_url,
      creator = request.POST['user_name'],
    )
    
    form_img = Image.objects.create(
      caption = caption_content[0],
      book = get_object_or_404(Book, pk=form_book.pk),
      img_url = uploaded_file_url
    )
    
    form_voice = Voice.objects.create(
      voice_url = tts_path[31:],
      book = get_object_or_404(Book, pk=form_book.pk),
    )
    
    context = {
      'form_img': form_img,
      'form_book': form_book,
      'form_voice': form_voice,
      'tts_path': tts_path[31:],
      'vc_path': vc_path[31:],
      'kr_tts_path': kr_tts_path[31:],
    }      
    
    return render(request, 'books/shot.html', context)
  return render(request, 'books/shot_mode.html')

# 앱 촬영 결과물 표
@csrf_exempt
def AndroidResult(request):
  recentBook = Book.objects.filter(creator=request.user.username).last()
  recentImg = Image.objects.filter(book=recentBook).last()
  recentVoice = Voice.objects.filter(book=recentBook).last().voice_url
  
  print("확인: ", recentBook)
  print("확인: ", recentImg)
  print("확인: ", recentVoice)
  
  context = {
    'recentBook': recentBook,
    'form_img': recentImg,
    'tts_path': recentVoice,
  }
  
  return render(request, 'books/shot.html', context)

@csrf_exempt
def tts(request):
  sentence = request.POST['sentence']

  if sentence:
    # TODO
    ## 이밎 파일 기반으로 tts 모듈호출

    path = '/static/media/src_voice.wav'

    return JsonResponse({'result': 'OK', 'data': path})

  return JsonResponse({'result': 'ERROR'})


