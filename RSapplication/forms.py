from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, RepairRequest, Technic, RepairOrder, Services, TechnicType
from django.contrib.auth.forms import AuthenticationForm


# ===============Регистрация клиента==============#
class ClientRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'firstname', 'lastname', 'phone_number']
        help_texts = []
        widgets = {
            "username": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Логин'
            }),
            "email": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Электронная почта'
            }),
            "password1": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            }),
            "password2": forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Повторите пароль'
            }),
            "firstname": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            "lastname": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            "phone_number": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефона'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''  # Убираем подсказки для поля password1
        self.fields['password2'].help_text = ''
        self.fields['username'].help_text = ''

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'client'  # Устанавливаем user_type на "client"
        if commit:
            user.save()
        return user


# ===============Форма заявки на обслуживание==============#
class RepairRequestForm(forms.ModelForm):
    # Дополнительные поля для марки и модели техники

    class Meta:
        model = RepairRequest
        fields = ['description', 'delivery', 'take_date']
        widgets = {
            'take_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }


class TechnicForm(forms.ModelForm):
    class Meta:
        model = Technic
        fields = ['type', 'brand', 'model']


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['name', 'service_description', 'coast']
        widgets = {
            "name": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Наименование услуги'
            }),
            "service_description": forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание услуги'
            }),
            "coast": forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Стоимость услуги'
            }),
        }


class TechTypeForm(forms.ModelForm):
    class Meta:
        model = TechnicType
        fields = ['name_type']
        widgets = {
            "name_type": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Наименование'
            }),
        }
