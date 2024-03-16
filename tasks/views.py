from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required #Esto sirve para que las funciones que tenga esto puedan entrar a su vista, solo si están logueados. Es como una forma de tiparlo

# Create your views here.


def home(request):
    return render(request, "home.html")

def signup(request):

    if request.method == "GET":
        return render(request, "signup.html", {
            "form": UserCreationForm
        })
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()
                # Esta función realiza las tareas necesarias para iniciar sesión al usuario, estableciendo las cookies de sesión y realizando cualquier otro trabajo necesario para autenticar al usuario en el sistema.
                login(request, user)
                return redirect("tasks_pending")
            except IntegrityError:  # Asegura que la aplicación pueda gestionar de manera adecuada la tentativa de crear un usuario con un nombre de usuario que ya está siendo utilizado por otro usuario en la base de datos, proporcionando así una experiencia de usuario más amigable.
                return render(request, "signup.html", {
                    "form": UserCreationForm,
                    "error": "Username already exists"
                })
        else:
            return render(request, "signup.html", {
                "form": UserCreationForm,
                "error": "Password do not match"
            })

@login_required
def tasks(request):
    # Esto sirve para que se muestren solo las tareas del usuario que está logueado en este momento y las tareas que aún no han sido realizadas.
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "tasks.html", {
        "tasks": tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by("-datecompleted") #Aquí busca las que ya están hechas y las ordena por sy fecha
    return render(request, "tasks.html", {
        "tasks": tasks
    })

@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {
            "form": TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            # Este sirve para que la tarea se guarde automaticamente en el usuario que está logueado
            new_task.user = request.user
            new_task.save()
            return redirect("tasks_pending")
        except:
            return render(request, "create_task.html", {
                "form": TaskForm,
                "error": "Please provide valide data"
            })

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user) # Esto busca desde Task, el id de la tarea y las tareas solo del usuario logueado
    form = TaskForm(instance=task)
    if request.method == "GET":
        return render(request, "task_detail.html", {
            "task": task,
            "form": form
        })
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks_pending")
        except ValueError:
            return render(request, "task_detail.html", {
                "task": task,
                "form": form,
                "error": "Error updating task"
            })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("tasks_pending")

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks_pending")

@login_required
def signout(request):
    logout(request)
    return redirect("home")

def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {
            "form": AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, "signin.html", {
                "form": AuthenticationForm,
                "error": "Username or password is incorrect"
            })
        else:
            login(request, user)
            return redirect("tasks_pending")
