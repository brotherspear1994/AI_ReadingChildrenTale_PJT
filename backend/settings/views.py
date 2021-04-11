from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import HttpResponse

# Create your views here.
def settings(request):
  return render(request, 'settings/settings.html')

def lang(request):
  user = request.user
  lang_choice = request.GET.get('lang')
  user.lang_choices = lang_choice
  user.save()
  # print(user.lang_choices)
  return HttpResponse(user.lang_choices)

@require_http_methods(['GET', 'POST'])
def mode(request):
  user = request.user
  md = request.GET.get('state')
  if md == "kid-mode":
    user.mode = True  #kid-mode: True
  else:
    user.mode = False #adult-mode: False
  user.save()
  return HttpResponse(user.mode)