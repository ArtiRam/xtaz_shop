from django import forms
from users import models
from django.contrib.auth.password_validation import validate_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите Пароль',
                                widget=forms.PasswordInput)

    class Meta:
        model = models.CustomUser
        fields = ('email', 'password', 'password2', 'phone', 'address', 'first_name', 'last_name')
        labels = {
            'email': 'E-mail',
            'password': 'Пароль',
            'password2': 'Повторите Пароль',
            'phone': 'Телефон',
            'address': 'Адрес',
            'first_name': 'Имя',
            'last_name': 'Фамилия'

        }

        widgets = {
            'password': forms.PasswordInput(),
            'password2': forms.PasswordInput()
        }

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    # --- check duplicate
    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
