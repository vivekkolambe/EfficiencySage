from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.IntegerField(blank = True,null=True)
    experience = models.DecimalField(max_digits=19, decimal_places=2,blank = True,null=True)
    is_manager = models.BooleanField()

