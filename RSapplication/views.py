from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.views import LoginView
from django.db.models import Sum, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import ClientRegistrationForm, RepairRequestForm, TechnicForm, ServiceForm, TechTypeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from .models import *
from django.http import HttpResponseBadRequest, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
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
            if user.position == 'manager':
                return reverse_lazy('ManagerHomePage')
            elif user.position == 'repairman':
                return reverse_lazy('RepairmanHomePage')

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
    done_orders = RepairOrder.objects.filter(request__owner=current_user)
    print(repair_requests)

    return render(request, 'RSapplication/home.html', {'technic_form': technic_form,
                                                       'repair_form': repair_form,
                                                       'repair_requests': repair_requests,
                                                       'current_user': current_user,
                                                       'done_orders': done_orders})


def pay_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')

        order = RepairOrder.objects.get(id=order_id)
        order.is_paid = True  # Необходимо изменить на is_paid
        order.save()
        return JsonResponse({'message': 'Заказ успешно оплачен'})
    else:
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)


@login_required
def edit_repair_request(request, request_id):
    repair_request = get_object_or_404(RepairRequest, id=request_id)
    technic = repair_request.technic

    if request.method == 'POST':
        if 'delete' in request.POST:
            repair_request.delete()
            return redirect('HomePage')

        repair_form = RepairRequestForm(request.POST, instance=repair_request)
        technic_form = TechnicForm(request.POST, instance=technic)
        if repair_form.is_valid() and technic_form.is_valid():
            repair_form.save()
            technic_form.save()
            return redirect('HomePage')
    else:
        repair_form = RepairRequestForm(instance=repair_request)
        technic_form = TechnicForm(instance=technic)

    return render(request, 'RSapplication/edit_repair_request.html', {
        'repair_form': repair_form,
        'technic_form': technic_form,
        'repair_request': repair_request
    })


@login_required()
def manager_page(request):
    repairmen = CustomUser.objects.filter(position='repairman')

    if request.method == 'POST':
        if 'action' in request.POST:
            if request.POST['action'] == 'create_order':
                try:
                    request_id = int(request.POST.get('request_id'))
                    repairman_id = int(request.POST.get('repairman'))
                    request_object = RepairRequest.objects.get(id=request_id)
                    repairman = CustomUser.objects.get(id=repairman_id)
                    RepairOrder.objects.create(request=request_object, repairman=repairman, status='Передан в работу')
                    created_order_id = RepairOrder.objects.latest('id').id
                    return HttpResponseRedirect(request.path_info)
                except (ValueError, RepairRequest.DoesNotExist, CustomUser.DoesNotExist) as e:
                    print("Ошибка при создании заказа:", e)
                    return HttpResponseBadRequest("Ошибка при создании заказа.")
            elif request.POST['action'] == 'accept_request':
                try:
                    request_id = int(request.POST.get('request_id'))
                    repair_request = RepairRequest.objects.get(id=request_id)
                    repair_request.technic_accepted = True
                    repair_request.save()
                    return redirect('ManagerHomePage')
                except (ValueError, RepairRequest.DoesNotExist) as e:
                    print("Ошибка при подтверждении заявки:", e)
                    return HttpResponseBadRequest("Ошибка при подтверждении заявки.")

    # Получаем только заявки, которые еще не имеют соответствующих заказов
    all_requests = RepairRequest.objects.exclude(Заявка_на_ремонт__isnull=False)

    return render(request, 'RSapplication/manager_home.html', {'all_requests': all_requests, 'repairmen': repairmen})


@login_required
def add_service(request):
    services = Services.objects.all()  # Определение переменной services за пределами блока условия

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ServicePage')
    else:
        form = ServiceForm()

    return render(request, 'RSapplication/service_actions.html', {'form': form, 'services': services})


@login_required
def add_tech_type(request):
    types = TechnicType.objects.all()
    form = TechTypeForm()

    if request.method == 'POST':
        if 'add_type' in request.POST:
            form = TechTypeForm(request.POST)
            if form.is_valid():
                print("Форма действительна. Данные:", form.cleaned_data)
                form.save()
                return redirect('TypesPage')
            else:
                print("Форма недействительна. Ошибки:", form.errors)
        elif 'delete_type' in request.POST:
            type_id = request.POST.get('delete_type')
            TechnicType.objects.filter(id=type_id).delete()
            return redirect('TypesPage')

    return render(request, 'RSapplication/technic_types.html', {'form': form, 'types': types})


@login_required
def repairman_orders(request):
    # Получаем текущего пользователя (мастера)
    current_user = request.user

    # Обработка запроса на обновление статуса заказа
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')

        # Получаем объект заказа или возвращаем ошибку 404, если его нет
        order = RepairOrder.objects.get(id=order_id)

        # Обновляем статус заказа и сохраняем его
        order.status = new_status
        order.save()

        # Обработка услуг для заказа
        selected_services = request.POST.getlist('selected_services')
        for service_id in selected_services:
            service = Services.objects.get(id=service_id)
            ServiceList.objects.create(service=service, repair_order=order)

            # После успешного обновления статуса перенаправляем пользователя
        return redirect('RepairmanHomePage')
        # После успешного обновления статуса перенаправляем пользователя

    # Получаем список всех доступных услуг
    services = Services.objects.all()

    # Фильтруем заказы по полю repairman для текущего пользователя
    orders = RepairOrder.objects.filter(repairman=current_user)

    # Создаем словарь, в котором каждому заказу соответствуют его услуги
    orders_with_services = ServiceList.objects.all()

    order_spec2 = {}

    for order in orders:
        order_spec2[order] = []
        service_lists = ServiceList.objects.filter(repair_order=order)
        # Создаем список, содержащий услуги для данного заказа
        services_for_order = [service_list.service for service_list in service_lists]
        for service in services:
            if service not in services_for_order:
                order_spec2[order].append(service)

    # Передаем список доступных услуг, заказы и словарь с услугами для каждого заказа в шаблон
    return render(request, 'RSapplication/repairman_home.html', {'orders': orders,
                                                                 'services': services,
                                                                 'orders_with_services': orders_with_services,
                                                                 'order_spec2': order_spec2})
