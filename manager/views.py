# manager/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from manager.models import *
from django.db import IntegrityError
from accounts.models import CustomUser
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

def createAndAssignTask(request):
    error_message = None
    form_data = {}  # Store form data to repopulate the fields on erro
    managers = CustomUser.objects.filter(is_manager=True)
    employees = CustomUser.objects.filter(is_manager=False)
    projects = Project.objects.filter(project_status='In Progress')
    if request.method == 'POST':
        form_data['task_name'] = request.POST.get('task_name')
        form_data['task_desc'] = request.POST.get('task_desc')
        form_data['task_status'] = request.POST.get('task_status')
        form_data['task_priority'] = request.POST.get('task_priority')
        
        Eid = request.POST.get('employee')
        employee = CustomUser.objects.get(id=Eid)
        form_data['employee'] = employee

        Pid = request.POST.get('project')
        project = Project.objects.get(id=Pid)
        form_data['project'] = project
        
        print(form_data)
        try:
            new_task = Task(
                task_name=form_data['task_name'],
                task_desc=form_data['task_desc'],
                task_status=form_data['task_status'],
                task_priority=form_data['task_priority'],
                employee=form_data['employee'],
                project=form_data['project'],
                manager=request.user,
            )
            new_task.save()

            messages.success(request, 'Project created successfully.')
            return redirect('manager-home')

        except IntegrityError:
            error_message = 'Project with this name already exists. Please choose a different name.'
            return render(request, 'createandAssignTask.html', {'employees': employees, 'managers': managers, 'projects': projects,'error_message':error_message})
    return render(request, 'createandAssignTask.html', {'employees': employees, 'managers': managers, 'projects': projects})

    