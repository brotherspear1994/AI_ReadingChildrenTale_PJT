from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
# AI 삽입을 위한 os import
import os
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media') # AI 삽입을 위한 MEDIA ROOT 설정

app_name = 'books'

urlpatterns = [
    path('', views.index, name="index"),
    # 1. 책 촬영
    path('shot/mode/', views.shot_mode, name="shot_mode"),
    # 2. 음성 녹음
    path('record/', views.record, name="record"),
    path('record/result/', views.recordResult, name="recordResult"),
    # 3. 라이브러리(책장)
    path('library/', views.library, name="library"),
    path('library/mybook/<int:pk>/', views.library_mybook, name='library_mybook'),
    path('library/all/', views.library_all, name="library_all"),
    # 4. 놀이터
    path('playground/', views.playground, name="playground"),
    path('mode/', views.mode, name="mode"),
    # 5. IC(이미지 캡셔닝)
    path('ic/', views.imageCaptioning, name="imageCaptioning"),
    path('ic/android/', views.imageCaptioningAndroid, name="imageCaptioningAndroid"),
    path('ic/android/result/', views.AndroidResult, name="AndroidResult"),
    # 6. tts
    path('tts/', views.tts, name="tts"),
    # 7. vc(voice conversion)
    # path('vc', views.voiceConversion, name="voiceConversion"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)