from django.urls import path, include
from .views import *

urlpatterns = [
    path('', main_page, name='MainPage'),
    path('registration', registration, name='registration'),
    path('login', LoginUser.as_view(), name='LoginUser'),
    path('logout', logout_view, name='LogoutUser'),
    path('home', login_required(create_repair_request), name='HomePage'),
    path('repair_request', create_repair_request, name='RepairRequier'),
    path('employee_home', manager_page, name='EmployeeHomePage')
]
