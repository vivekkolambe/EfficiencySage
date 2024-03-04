
# manager/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='manager-home'),
    path('create_project/', views.create_project_view, name='create_project'),
]
