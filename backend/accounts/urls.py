from django.urls import path
from . import views
from rest_framework import routers
from accounts import views

app_name = 'accounts'
router = routers.DefaultRouter()
router.register('account',views.UserViewset)

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('delete/', views.delete, name='delete'),
    path('account/', views.UserViewset, name='account'),
    path('get-user/', views.get_user, name="get_user"),  # 추가하기
]
