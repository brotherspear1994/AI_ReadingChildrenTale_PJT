from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        # fields = '('email', 'mode', 'birth_year',)'
        fields = '__all__'

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = '기존 비밀번호'
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
        })
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })

class SignupForm(UserCreationForm):
    email = forms.EmailField(
		label='',
		max_length=254,
		widget=forms.EmailInput(
			attrs={
				"placeholder": "본인 확인용 이메일",
				"class": "form-control"
			}
		)
	)


    username = forms.CharField(
		label='',
		max_length=30,
		min_length=5,
		required=True,
		widget=forms.TextInput(
			attrs={
				"placeholder": "아이디",
				"class": "form-control"
			}
		)
	)


    password1 = forms.CharField(
		label='',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"placeholder": "비밀번호(8자 이상)",
				"class": "form-control"
			}
		)
	)

    password2 = forms.CharField(
		label='',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"placeholder": "비밀번호 확인",
				"class": "form-control"
			}
		)
	)

    birth_year = forms.DateField(
        label='생년월일',
        required=False,
        widget=forms.widgets.DateInput(attrs={'type': 'date'})
    )

    field_order = ['username', 'password1', 'password2', 'email', 'birth_year']

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email', 'birth_year')