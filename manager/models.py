from django.db import models
import os
from datetime import datetime

def upload_location(instance, filename):
    current_date = datetime.now().strftime('%Y%m%d')
    filename, extension = os.path.splitext(filename)
    new_filename = f"{instance.name}_{current_date}{extension}"
    return f"Project Documents/{new_filename}"

class Project(models.Model):
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    project_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress')
    manager = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='projects_created')
    document = models.FileField(upload_to=upload_location, null=True, blank=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    PRIORITY_CHOICES = [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ]
    task_name = models.CharField(max_length=50,unique=True)
    task_desc = models.CharField(max_length=100)
    task_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    task_priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='2')
    employee = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='assigned_tasks',limit_choices_to={'is_manager': False})
    manager = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='managed_tasks', limit_choices_to={'is_manager': True})
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name



#olddd
# # manager/models.py
# from django.db import models
# from accounts.models import CustomUser  # Assuming your CustomUser model is in the accounts app
# import os
# from datetime import datetime
# def upload_location(instance, filename):
#     # Get current date
#     current_date = datetime.now().strftime('%Y%m%d')
    
#     # Construct the new filename using field4 and the current date
#     filename, extension = os.path.splitext(filename)
#     new_filename = f"{instance.name}_{current_date}{extension}"
#     return f"Project Documents/{new_filename}"

# class Project(models.Model):
#     STATUS_CHOICES = [
#         ('In Progress', 'In Progress'),
#         ('Completed', 'Completed'),
#     ]
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255, unique=True)
#     description = models.TextField()
#     project_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress')
#     manager_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects_created')
#     document = models.FileField(upload_to=upload_location, null=True, blank=True)

#     def __str__(self):
#         return self.name

# class Task(models.Model):
#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('In Progress', 'In Progress'),
#         ('Completed', 'Completed'),
#     ]
#     PRIORITY_CHOICES = [
#         ('0', '0'),
#         ('1', '1'),
#         ('2', '2'),
#         ('3', '3'),
#         ('4', '4'),
#     ]
#     task_name = models.CharField(max_length=50,unique=True)
#     task_desc = models.CharField(max_length=100)
#     task_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
#     task_priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='2')
#     employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_tasks',limit_choices_to={'is_manager': False})
#     manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='managed_tasks', limit_choices_to={'is_manager': True})
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.task_name
