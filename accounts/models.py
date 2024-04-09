from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=10, blank=True, null=True)
    experience = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    is_manager = models.BooleanField()
    is_allocated=models.BooleanField(default=False)
    project = models.ForeignKey('manager.Project', on_delete=models.SET_NULL, null=True, blank=True)

# oldd
# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from manager.models import Project

# class CustomUser(AbstractUser):
#     phone = models.CharField(max_length=10, blank=True, null=True)
#     experience = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
#     is_manager = models.BooleanField()
#     is_allocated=models.BooleanField(default=False)
#     project_id = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)



