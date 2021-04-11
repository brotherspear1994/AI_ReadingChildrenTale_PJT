from django import forms
from .models import Book, Image, Voice, VoicePattern

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = '__all__'

class VoiceForm(forms.ModelForm):

    class Meta:
        model = Voice
        fields = '__all__'

class VoicePatternForm(forms.ModelForm):

    class Meta:
        model = VoicePattern
        fields = ['speaker_name', 'voice_pattern_url']