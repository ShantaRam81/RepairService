from django.contrib import admin
from RSapplication.models import CustomUser, Technic, RepairRequest

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Technic)
admin.site.register(RepairRequest)