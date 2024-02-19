from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
class CustomUser(AbstractUser):
    firstname = models.CharField(max_length=100, verbose_name='Имя')
    lastname = models.CharField(max_length=100, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=11, verbose_name='Номер телфона', unique=True)
    email = models.EmailField(max_length=100, verbose_name='Электронная почта', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    USER_TYPE_CHOICES = [
        ('employee', 'Сотрудник'),
        ('client', 'Клиент'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, verbose_name="Тип пользователя", null=True,
                                 blank=True)
    position = models.CharField(max_length=100, verbose_name="Должность", null=True, blank=True)

    def __str__(self):
        return self.firstname

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


# Изменяем related_name для обратных связей групп и разрешений
CustomUser.groups.field.remote_field.related_name = 'customuser_groups'
CustomUser.user_permissions.field.remote_field.related_name = 'customuser_permissions'


class Technic(models.Model):
    brand = models.CharField(max_length=100, verbose_name='Марка техники')
    model = models.CharField(max_length=100, verbose_name='Модель техники')

    class Meta:
        verbose_name = 'Техника'
        verbose_name_plural = 'Техника'


class RepairRequest(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='repair_requests', verbose_name='Владелец техники')
    technic = models.ForeignKey(Technic, on_delete=models.PROTECT, related_name='repair_requests', verbose_name='Техника клиента')
    description = models.TextField(max_length=300, verbose_name='Описание проблемы')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='Дата/время создания')

    class Meta:
        verbose_name = 'Заявка на обслуживание'
        verbose_name_plural = 'Заявки на обслуживание'


