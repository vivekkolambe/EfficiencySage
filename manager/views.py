from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
# Create your views here.
# manager/views.py

def home(request):
    User = get_user_model()
    is_manager = request.user.is_manager
    if is_manager:
        # Logic to retrieve data for the manager's home page
        pie_data = {
            'labels': ['Completed', 'In Progress', 'Pending'],
            'values': [30, 50, 20]
        }
        return render(request, 'home.html', {'pie_data': pie_data})
    else:
        # Logic to retrieve data for non-manager's home page
        # You can define this logic according to your application requirements
        return render(request, 'non_manager_home.html')