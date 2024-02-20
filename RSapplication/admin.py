from django.contrib import admin
from RSapplication.models import CustomUser, Technic, RepairRequest, RepairOrder, TechnicType, Services, ServiceList

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Technic)
admin.site.register(RepairRequest)
admin.site.register(RepairOrder)
admin.site.register(TechnicType)
admin.site.register(Services)
admin.site.register(ServiceList)

