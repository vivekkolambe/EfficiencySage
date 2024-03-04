# manager/models.py
from django.db import models
from accounts.models import CustomUser  # Assuming your CustomUser model is in the accounts app

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    manager_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects_created')
    document = models.FileField(upload_to='project_documents/', null=True, blank=True)

    def __str__(self):
        return self.name
