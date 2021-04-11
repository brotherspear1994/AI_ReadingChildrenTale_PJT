from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET,require_POST, require_http_methods
#serializers 임포트합니당
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from .forms import CustomUserChangeForm, CustomPasswordChangeForm, SignupForm
from .decorators import login_message_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view
def get_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)
    
@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('books:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'books:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')


@login_required
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('books:index')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('books:index')
    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

# @login_message_required
@login_required
@require_http_methods(['GET', 'POST'])
def profile(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.INFO, '비밀번호가 변경되었습니다!')
            auth_login(request, user)
            return redirect('accounts:profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
@require_POST
def delete(request):
    request.user.delete()
    logout(request)
    messages.success(request, "회원탈퇴가 완료되었습니다.")
    return redirect('books:index')

@api_view
def get_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)