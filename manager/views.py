# manager/views.py

import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from manager.models import *
from django.db import IntegrityError
from accounts.models import CustomUser
from django.shortcuts import get_object_or_404
from .models import Project


@login_required(login_url='/accounts/login')
def home(request):
    User = get_user_model()
    is_manager = request.user.is_manager
    
    # Get tasks associated with these projects
    if is_manager:
        projects = Project.objects.filter(manager=request.user)
        tasks = Task.objects.filter(project__in=projects)
        tasks_json = json.dumps(list(tasks.values()))
        # Retrieve employees assigned to the projects managed by the current user
        assigned_employees = User.objects.filter(project__in=projects, is_manager=False)

        return render(request, 'man_home.html', {'tasks': tasks_json, 'projects': projects, 'assigned_employees': assigned_employees})
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
            # Get the current user (manager)
            manager = request.user

            # Create the project
            new_project = Project(
                name=form_data['project_name'],
                description=form_data['project_description'],
                manager_id=manager.id,  # Assign the manager's ID, not the object itself
                document=form_data['project_document']
            )
            new_project.save()

             #update user project allocation status to True and project id assigned to manager
            request.user.is_allocated=True;
            request.user.project_id=new_project.id;
            request.user.save()


            messages.success(request, 'Project created successfully.')
            return redirect('manager-home')

        except IntegrityError:
            error_message = 'Project with this name already exists. Please choose a different name.'

    return render(request, 'createProject.html', {'error_message': error_message, 'form_data': form_data})

def createAndAssignTask(request):
    error_message = None
    form_data = {}  # Store form data to repopulate the fields on erro
    managers = CustomUser.objects.filter(is_manager=True)
    employees = CustomUser.objects.filter(is_manager=False, project=request.user.project)
    assigned_project = request.user.project

    # Check if the logged-in user has an assigned project
    if assigned_project:
        projects = Project.objects.filter(project_status='In Progress', id=assigned_project.id)
    else:
        projects = None  # No assigned project for the logged-in user
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


def assign_employee(request):
    # Query all free employees who are not managers
    free_employees = CustomUser.objects.filter(is_manager=False, is_allocated=False)

    # Render the template with the list of free employees
    return render(request, 'assignEmployee.html', {'free_employees': free_employees})

def update_employees(request):
    if request.method == 'POST':
        selected_employee_ids = request.POST.getlist('selected_employees')
        project = request.user.project  # Assuming project is a ForeignKey field on the user model

        # Update selected employees
        CustomUser.objects.filter(id__in=selected_employee_ids).update(
            is_allocated=True,
            project=project
        )

        # Redirect back to man_home.html
        return redirect('manager-home')
    else:
        # Handle GET request if needed
        pass

def employee_tasks(request, employee_id):
    # Retrieve tasks assigned to the clicked employee
    tasks = Task.objects.filter(employee_id=employee_id)
    employee = get_object_or_404(CustomUser, id=employee_id)
    # Pass tasks and employee context to the template
    return render(request, 'employee_tasks.html', {'tasks': tasks, 'employee': employee})

def employee_dashboard(request):
    # Get employees under the current manager (request.user)
    employees = CustomUser.objects.filter(assigned_tasks__manager=request.user)
    
    # Create a dictionary to hold tasks data for each employee
    employees_tasks = {}
    
    # Iterate over each employee
    for employee in employees:
        # Get tasks data for the current employee
        tasks = Task.objects.filter(employee=employee)
        
        # Convert tasks data to JSON format
        tasks_json = json.dumps(list(tasks.values()))
        
        # Add tasks data to the dictionary
        employees_tasks[employee.username] = tasks_json
    
    # Pass employees_tasks dictionary as context to the template
    return render(request, 'employee_dashboard.html', {'employees_tasks': employees_tasks})
