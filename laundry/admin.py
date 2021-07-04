from django.contrib import admin
from .models import Laundry, Machine, Option

# Register your models here.
admin.site.register(Laundry)
admin.site.register(Machine)
admin.site.register(Option)
