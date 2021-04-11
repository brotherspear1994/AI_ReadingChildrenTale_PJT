from django.conf.urls import url
from django.urls import path
from . import views

import os
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

app_name="web"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('ic', views.imageCaptioning),
    path('tts', views.tts),
    path('vc', views.voiceConversion),
]
