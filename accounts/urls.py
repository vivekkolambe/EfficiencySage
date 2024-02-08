from django.urls import path,include
from .views import *
urlpatterns = [
   path('login',LoginView,name='login-page'),
   path('register',RegisterView,name='register-page'),
   path('form',formView ,name='form-page'),
   path('logout-user',logoutView,name='logout'),
   path('working',workView,name='working'),

]
