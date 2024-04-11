import json
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def LoginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'User Does Not Exist')
            return redirect('login-page')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_manager:
                return redirect('manager-home')  # Redirect to manager home page
            else:
                return redirect('employee-home')  # Redirect to the employee home page
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login-page')
    return render(request, 'login.html')

def RegisterView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        user_type = request.POST.get('user_type')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return redirect('register-page')
        elif password != confirm_password:
            messages.error(request, 'Password does not match')
            return redirect('register-page')
        else:
            is_manager = False
            if user_type == 'manager':
                is_manager = True
            
                
            user = CustomUser.objects.create_user(username=username, password=password,email = email,is_manager = is_manager)
            user = authenticate(request, username=username, password=password)
            login(request,user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('form-page')
    return render(request,'register.html')

@login_required(login_url='/accounts/login')
def formView(request):
    user = request.user

    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        phone = request.POST.get('phone-number')
        experience = request.POST.get('experience')
        skill_input = request.POST.get('skill_input')
        skill_list = skill_input.split(',')
        skill_json = json.dumps(skill_list)
        
        # Update user object fields
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.experience = experience
        user.skills = skill_json
        # Save changes to the database
        user.save()

        # Redirect to 'working' view
        return redirect('working')

    context = {
        'username': user.username,
        'email': user.email,
        'role': 'Manager' if user.is_manager else 'Employee',
    }

    return render(request, 'form.html', context)

@login_required(login_url='/accounts/login')
def logoutView(request):
    logout(request)
    messages.success(request,"You have successfully been logged out !!")
    return redirect('login-page')


@login_required(login_url='/accounts/login')
def workView(request):
    return render(request,'delete.html')

@login_required(login_url='/accounts/login')
def profileView(request):
    profile_user  = request.user
    return render(request,'profile_demo.html')

def editProfileView(request):
    return render(request,'edit_profile.html')

def editProfileView(request):
    user = request.user
    if request.method == 'POST':
        # Process form submission
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        experience = request.POST.get('experience')
        skills = request.POST.get('skills')

        # Update user object with new data
        user.username = username
        user.email = email
        user.phone = phone
        user.experience = experience
        user.skills = skills

        # Save user object
        user.save()
        return redirect('profile-page')
    else:
        # Render edit user form
        return render(request, 'edit_profile.html', {'user': user})