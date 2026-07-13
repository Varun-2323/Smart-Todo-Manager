from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Task,Profile
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import json
from django.shortcuts import redirect
from .models import Task


def todo_page(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "index.html")



def Login_page(request):

    # If already logged in, go to dashboard
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)
            return redirect("dashboard")

        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")
def Register_page(request):


    if request.method == "POST":

        fullname = request.POST.get("fullname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration Successful!")

        return redirect("login")

    return render(request, "register.html")


def Dashboard_page(request):

    tasks = Task.objects.filter(user=request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Search
    search_query = request.GET.get("search", "")

    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    # Counts
    pending_count = tasks.filter(status="Pending").count()
    completed_count = tasks.filter(status="Completed").count()

    # Status Filter
    status = request.GET.get("status")

    if status == "Pending":
        tasks = tasks.filter(status="Pending")

    elif status == "Completed":
        tasks = tasks.filter(status="Completed")
    
    task_data = []

    for task in tasks.filter(status="Pending"):
       task_data.append({
        "id": task.id,
        "title": task.title,
        "date": str(task.reminder_date),
        "time": task.reminder_time.strftime("%H:%M"),
        })
    context = {
        "tasks": tasks,
        "pending_count": pending_count,
        "completed_count": completed_count,
        "status": status,
        "search_query": search_query,
         "profile": profile,
        "task_data": json.dumps(task_data),
    }

    return render(request, "dashboard.html", context)



def Add_Task(request):

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = request.POST.get("priority")
        reminder_date = request.POST.get("reminder_date")
        reminder_time = request.POST.get("reminder_time")

        Task.objects.create(

            user=request.user,

            title=title,

            description=description,

            priority=priority,

            reminder_date=reminder_date,

            reminder_time=reminder_time

        )

        return redirect("dashboard")

    return render(request,"add_task.html")




def Edit_Task(request, id):

    task = Task.objects.get(id=id)

    if request.method == "POST":

        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.priority = request.POST.get("priority")
        task.reminder_date = request.POST.get("reminder_date")
        task.reminder_time = request.POST.get("reminder_time")

        task.save()

        return redirect("dashboard")

    return render(request, "edit_task.html", {"task": task})

def Delete_Task(request, id):

    task = Task.objects.get(id=id)

    task.delete()

    return redirect("dashboard")

def Complete_Task(request, id):

    task = Task.objects.get(id=id)

    task.status = "Completed"

    task.save()

    return redirect("dashboard")


def Logout_page(request):
    logout(request)
    return redirect("login")



@login_required
def Edit_Profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        request.user.username = request.POST.get("username")
        request.user.email = request.POST.get("email")
        request.user.save()

        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES["profile_image"]
            profile.save()
        if request.POST.get("remove_picture"):
            profile.profile_image = "profile_pics/default.png"
            profile.save()

        messages.success(request, "Profile Updated Successfully.")

        return redirect("dashboard")

    context = {
    "profile": profile,
    "user": request.user,
    }

    return render(request, "edit_profile.html", context)



