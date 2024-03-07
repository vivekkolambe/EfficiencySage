# manager/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from manager.models import Project
from django.db import IntegrityError

@login_required(login_url='/accounts/login')
def home(request):
    User = get_user_model()
    is_manager = request.user.is_manager
    if is_manager:
        # Logic to retrieve data for the manager's home page
        pie_data = {
            'labels': ['Completed', 'In Progress', 'Pending'],
            'values': [30, 50, 20]
        }

        # projects = Project.objects.all()
        projects = Project.objects.filter(manager_id=request.user)

        return render(request, 'man_home.html', {'pie_data': pie_data, 'projects': projects})
    else:
        # Logic to retrieve data for non-manager's home page
        # You can define this logic according to your application requirements
        return redirect('login-page')



@login_required(login_url='/accounts/login')
def create_project_view(request):
    error_message = None
    form_data = {}  # Store form data to repopulate the fields on error

    if request.method == 'POST':
        form_data['project_name'] = request.POST.get('project_name')
        form_data['project_description'] = request.POST.get('project_description')
        form_data['project_document'] = request.FILES.get('project_document')

        try:
            new_project = Project(
                name=form_data['project_name'],
                description=form_data['project_description'],
                manager_id=request.user,
                document=form_data['project_document']
            )
            new_project.save()

            messages.success(request, 'Project created successfully.')
            return redirect('manager-home')

        except IntegrityError:
            error_message = 'Project with this name already exists. Please choose a different name.'

    return render(request, 'createProject.html', {'error_message': error_message, 'form_data': form_data})

