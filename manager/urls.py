
# manager/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='manager-home'),
    path('create_project/', views.create_project_view, name='create_project'),
    path('create_task/', views.createAndAssignTask, name='create_task'),
    path('assign-employees/', views.assign_employee, name='assign_employees'),
    path('update-employees/', views.update_employees, name='update_employees'),
]
