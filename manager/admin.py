from django.contrib import admin

# Register your models here.
# manager/admin.py
from .models import *

admin.site.register(Project)
admin.site.register(Task)


