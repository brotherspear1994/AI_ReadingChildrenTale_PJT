from django.db import models
from django.conf import settings
# Create your models here.

class Book(models.Model):
    title = models.TextField(max_length=20, null=True)
    thumbnail_url = models.ImageField(upload_to='books/%Y/%m/%d/', null=True)
    is_open = models.TextField(max_length=10, default='1', null=True)
    # creator -> 생성한 user ForeignKey 넣어야할 것 같다!
    creator = models.CharField(max_length=50, null=True)
    author = models.CharField(max_length=50, null=True)
    summary = models.TextField(null=True)

    def __str__(self):
        return self.title

class Image(models.Model):
    img_url = models.ImageField(null=True, upload_to='images/%Y/%m/%d/')
    page = models.IntegerField(null=True)
    caption = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

# class UserBook(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)

class Voice(models.Model):
    page = models.IntegerField(null=True)
    voice_url = models.FileField(null=True, upload_to='voices/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

# 목소리 패턴을 위한 음성녹음파일
class VoicePattern(models.Model):
    speaker_name = models.CharField(max_length = 30)
    voice_pattern_url = models.FileField(null=True, upload_to='voice_patterns/%Y/%m/%d/')
    voice_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)