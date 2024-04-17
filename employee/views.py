import json
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from manager.models import Task
from django.db.models import Q
# Create your views here.
@login_required(login_url='/accounts/login')
def home(request):
    User = get_user_model()
    is_manager = request.user.is_manager
    pending_tasks = Task.objects.filter(
        Q(employee=request.user.id) & 
        (Q(task_status='Pending'))
    )
    in_progress_tasks = Task.objects.filter(
        Q(employee=request.user.id) & 
        (Q(task_status='In Progress'))
    )
    completed_tasks = Task.objects.filter(
        Q(employee=request.user.id) & 
        (Q(task_status='Completed'))
    )
    completed_count = Task.objects.filter(task_status='Completed').count()
    in_progress_count = Task.objects.filter(task_status='In Progress').count()
    pending_count = Task.objects.filter(task_status='Pending').count()
    
    # Prepare data for the chart
    pie_chart_data = {
        'labels': ['Completed', 'In Progress', 'Pending'],
        'datasets': [{
            'data': [completed_count, in_progress_count, pending_count],
            'backgroundColor': ['#28a745', '#ffc107', '#dc3545']
        }]
    }
    
    # Convert data to JSON format
    pie_chart_data_json = json.dumps(pie_chart_data)
    if  is_manager:
        # Logic to retrieve data for the manager's home page
        return redirect('login-page')
        
    else:
        # Logic to retrieve data for non-manager's home page
        # You can define this logic according to your application requirements
        pie_data = {
            'labels': ['Completed', 'In Progress', 'Pending'],
            'values': [30, 50, 20]
        }
        return render(request, 'emp_home.html', {'pie_data': pie_data,"in_progress_tasks":in_progress_tasks,"completed_tasks":completed_tasks,"pending_tasks":pending_tasks,"pie_chart_data":pie_chart_data_json})


def task_details(request, task_id):
    # Retrieve the task object from the database
    task = get_object_or_404(Task, pk=task_id)
    
    # Render the task details template with the task object
    return render(request, 'task_details.html', {'task': task})

def start_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.task_status = 'In Progress'
    task.save()
    return redirect('task_detail', task_id=task_id)

def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.task_status = 'Completed'
    task.save()
    return redirect('task_detail', task_id=task_id)

def dynamic_chart(request):
    # Query your database to get the count of tasks for each status
    
    completed_count = Task.objects.filter(status='Completed').count()
    in_progress_count = Task.objects.filter(status='In Progress').count()
    pending_count = Task.objects.filter(status='Pending').count()
    
    # Prepare data for the chart
    pie_chart_data = {
        'labels': ['Completed', 'In Progress', 'Pending'],
        'datasets': [{
            'data': [completed_count, in_progress_count, pending_count],
            'backgroundColor': ['#28a745', '#ffc107', '#dc3545']
        }]
    }
    
    # Convert data to JSON format
    pie_chart_data_json = json.dumps(pie_chart_data)
    
    # Pass data to the template
    return render(request, 'dynamic_chart.html', {'pie_chart_data': pie_chart_data_json})