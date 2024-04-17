from django.urls import path,include
from .views import *
from employee import views
urlpatterns = [
   path('', views.home, name='employee-home'),
   path('task/<int:task_id>/', task_details, name='task_detail'),
   path('task/<int:task_id>/start/', start_task, name='start_task'),
   path('task/<int:task_id>/complete/', complete_task, name='complete_task'),
]
