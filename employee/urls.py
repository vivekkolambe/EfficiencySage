from django.urls import path,include
from .views import *
from employee import views
urlpatterns = [
   path('', views.home, name='employee-home'),

]
