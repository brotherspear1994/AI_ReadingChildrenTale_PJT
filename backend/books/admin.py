from django.contrib import admin
from accounts.models import User
from books.models import Book, Image, VoicePattern, Voice

# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Image)
admin.site.register(VoicePattern)
admin.site.register(Voice)
# admin.site.register(UserBook)