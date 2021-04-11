from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
  path('', views.settings, name='settings'),
  path('lang/', views.lang, name='lang'),
  path('mode/', views.mode, name='mode'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

