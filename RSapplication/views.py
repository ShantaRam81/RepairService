from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .forms import ClientRegistrationForm, RepairRequestForm, TechnicForm, RepairOrderForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from .models import *

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from django.contrib.auth.hashers import make_password


def main_page(request):
    return render(request, 'RSapplication/main_page.html')


def registration(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Сначала создаем пользователя, но не сохраняем его в базе данных
            password = form.cleaned_data['password1']  # Получаем пароль из формы
            user.set_password(password)  # Устанавливаем зашифрованный пароль
            user.save()  # Сохраняем пользователя в базе данных

            # Авторизуем пользователя
            authenticated_user = authenticate(email=user.email, password=password)
            login(request, authenticated_user)

            # После успешной регистрации перенаправляем пользователя на страницу приветствия
            return redirect('LoginUser')
    else:
        form = ClientRegistrationForm()
    return render(request, 'RSapplication/client_register.html', {'form': form})


# ===============АВТОРИЗАЦИЯ==============#
def logout_view(request):
    logout(request)
    # После выхода из системы перенаправляем пользователя на страницу входа или на другую страницу
    return redirect('LoginUser')


class LoginUser(SuccessMessageMixin, FormView):
    form_class = AuthenticationForm
    template_name = 'RSapplication/login.html'
    success_message = 'Успешная авторизация'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка аутентификации')
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user
        print(user.user_type)
        if user.user_type == "client":
            return reverse_lazy('HomePage')
        else:
            return reverse_lazy('EmployeeHomePage')

    def form_valid(self, form):
        # Получаем данные пользователя из формы аутентификации
        email = form.cleaned_data['username']
        password = form.cleaned_data['password']
        print(password)
        print(email)

        # Пытаемся аутентифицировать пользователя
        user = authenticate(username=email, password=password)
        print(user)
        if user is not None:
            # Успешная аутентификация
            login(self.request, user)
            print('Succes')
            return super().form_valid(form)
        else:
            # Неудачная аутентификация
            return self.form_invalid(form)


@login_required
def home_page_client(request):
    return render(request, 'RSapplication/home.html', {"title": "Home Page"})


# ===============ЗАЯВКА==============#
@login_required
def create_repair_request(request):
    if request.method == 'POST':
        technic_form = TechnicForm(request.POST)
        repair_form = RepairRequestForm(request.POST)
        if technic_form.is_valid() and repair_form.is_valid():
            technic = technic_form.save()
            repair_request = repair_form.save(commit=False)
            repair_request.owner = request.user
            repair_request.created_time = timezone.now()
            repair_request.technic = technic
            repair_request.save()
            return redirect('HomePage')
    else:
        technic_form = TechnicForm()
        repair_form = RepairRequestForm()

    # Вывод списка заявок конкретного клиента
    current_user = request.user
    repair_requests = RepairRequest.objects.filter(owner=current_user)
    print(repair_requests)

    return render(request, 'RSapplication/home.html', {'technic_form': technic_form,
                                                       'repair_form': repair_form,
                                                       'repair_requests': repair_requests})


def manager_page(request):
    all_requests = RepairRequest.objects.all()
    repairmen = CustomUser.objects.filter(position='Repairman')

    if request.method == 'POST' and 'action' in request.POST:
        if request.POST['action'] == 'create_order':
            form = RepairOrderForm(request.POST)
            if form.is_valid():
                request_id = form.cleaned_data['request_id']
                repairman_id = form.cleaned_data['repairman']
                print("Request ID:", request_id)
                print("Repairman ID:", repairman_id)
                request_object = RepairRequest.objects.get(id=request_id)
                repairman = CustomUser.objects.get(id=repairman_id)
                RepairOrder.objects.create(request=request_object, repairman=repairman, status='в работе')
                return redirect('employee_home')

    else:
        form = RepairOrderForm()

    return render(request, 'RSapplication/employee_home.html', {'all_requests': all_requests, 'repairmen': repairmen, 'form': form})
