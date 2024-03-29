from django.urls import path, include
from .views import *

urlpatterns = [
    path('', main_page, name='MainPage'),
    path('registration', registration, name='registration'),
    path('login', LoginUser.as_view(), name='LoginUser'),
    path('logout', logout_view, name='LogoutUser'),
    path('home', login_required(create_repair_request), name='HomePage'),
    path('repair_request', create_repair_request, name='RepairRequier'),
    path('repair_request/<int:request_id>/edit/', edit_repair_request, name='edit_repair_request'),
    path('manager_home', manager_page, name='ManagerHomePage'),
    path('service_actions/', add_service, name='ServicePage'),
    path('technic_types_actions', add_tech_type, name='TypesPage'),
    path('repairman_home', repairman_orders, name='RepairmanHomePage'),
    path('pay_order', pay_order, name='PayOrder'),
    path('profile_page', profile_page, name='ProfilePage'),
    path('update_order_coast/<int:order_id>/', update_order_coast, name='update_order_coast'),
]
