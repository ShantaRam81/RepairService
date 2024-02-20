from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
class CustomUser(AbstractUser):
    firstname = models.CharField(max_length=100, verbose_name='Имя')
    lastname = models.CharField(max_length=100, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона', unique=True)
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
        return f"{self.firstname} {self.lastname}, {self.get_user_type_display()}, {self.position}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


CustomUser.groups.field.remote_field.related_name = 'customuser_groups'
CustomUser.user_permissions.field.remote_field.related_name = 'customuser_permissions'


class TechnicType(models.Model):
    name_type = models.TextField(max_length=50, verbose_name='Наименование типа')

    class Meta:
        verbose_name = 'Тип техники'
        verbose_name_plural = 'Типы техники'

    def __str__(self):
        return self.name_type


class Technic(models.Model):
    type = models.ForeignKey(TechnicType, null=True, blank=True, on_delete=models.PROTECT, verbose_name='тип техники')
    brand = models.CharField(max_length=100, verbose_name='Марка техники')
    model = models.CharField(max_length=100, verbose_name='Модель техники')

    class Meta:
        verbose_name = 'Техника'
        verbose_name_plural = 'Техника'

    def __str__(self):
        return f"{self.brand} {self.model}"


class RepairRequest(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='repair_requests', verbose_name='Владелец техники')
    technic = models.ForeignKey(Technic, on_delete=models.CASCADE, related_name='repair_requests', verbose_name='Техника клиента')
    description = models.TextField(max_length=300, verbose_name='Описание проблемы')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='Дата/время создания')

    class Meta:
        verbose_name = 'Заявка на обслуживание'
        verbose_name_plural = 'Заявки на обслуживание'

    def __str__(self):
        return (f"{self.owner.firstname} {self.owner.lastname} | "
                f"{self.technic.brand}  {self.technic.model} | {self.description} | {self.created_time}")




class RepairOrder(models.Model):
    request = models.ForeignKey(RepairRequest, on_delete=models.CASCADE, related_name='Заявка_на_ремонт', verbose_name='Request')
    repairman = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='Мастер', verbose_name='Repairman')
    status = models.CharField(max_length=20, null=True)
    created_time = models.DateTimeField(default=timezone.now, null=True, verbose_name='Order created time')
    end_time = models.DateTimeField(default=timezone.now, null=True, verbose_name='End time')

    class Meta:
        verbose_name = 'Заказ на обслуживание'
        verbose_name_plural = 'Заказы на обслуживание'

    def __str__(self):
        return (f"Клиент - {self.request.owner.firstname} {self.request.owner.lastname} | "
                f"{self.request.technic.brand}  {self.request.technic.model} | "
                f"{self.request.description} | {self.created_time} | "
                f" Мастер - {self.repairman.firstname} {self.repairman.lastname}")


class Services(models.Model):
    name = models.TextField(max_length=300, verbose_name='Наименование услуги')
    service_description = models.TextField(max_length=500, verbose_name='Описание услуги')
    coast = models.CharField(max_length=6, verbose_name='Стоимость оказания услуги')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return f"{self.name} - {self.coast} руб"


class ServiceList(models.Model):
    repair_order = models.ForeignKey(RepairOrder, null=True, blank=True, on_delete=models.CASCADE, related_name='service_lists')
    service = models.ForeignKey(Services, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Список услуг'
        verbose_name_plural = 'Списки услуг'


