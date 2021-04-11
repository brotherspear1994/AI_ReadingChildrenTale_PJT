from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Book

# Create your models here.
class User(AbstractUser):
    mode = models.BooleanField(null=True, default=True)
    birth_year = models.DateField(auto_now=False, null=True, blank=True)
    books = models.ManyToManyField(Book, related_name='user')
    voice_select = models.IntegerField(null=True)

    KOREA = 'KO'
    USA = 'EN'
    ARAB = 'AR'
    JAPAN = 'JA'
    VIETNAM = 'VI'

    LANG_CHOICES = [
        (KOREA, 'Korean'),
        (USA, 'English'),
        (ARAB, 'Arabic'),
        (JAPAN, 'Japan'),
        (VIETNAM, 'Vietnam'),
    ]

    lang_choices = models.CharField(
        max_length=10,
        choices=LANG_CHOICES,
        default=KOREA,
        null=True,
    )

    def is_upperclass(self):
        return self.lang_choices in {self.KOREA, self.VIETNAM}    
    