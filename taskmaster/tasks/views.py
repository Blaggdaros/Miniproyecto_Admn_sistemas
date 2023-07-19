from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect, render
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from tasks import forms
from tasks.models import Subject, Task

from .models import Task
from .serializers import TaskSerializer


def homepage(request):
    tasks = Task.objects.all().order_by("-created")[0:4]
    return render(
        request,
        "tasks/homepage.html",
        {
            "title": "TaskMaster homepage",
            "tasks": tasks,
        },
    )


LISTA_TAREAS = [
    {"id": 1, "title": "Aprender Python", "urgent": True},
    {"id": 2, "title": "Aprender Django", "urgent": True},
    {"id": 3, "title": "Comprar melocotones", "urgent": False},
]


def list_tasks(request):
    tasks = Task.objects.all()
    return render(
        request,
        "tasks/list_tasks.html",
        {
            "title": "Tareas activas",
            "tasks": tasks,
        },
    )


def list_subjects(request):
    subjects = Subject.objects.all()
    return render(
        request,
        "tasks/list_subjects.html",
        {
            "title": "Temas",
            "subjects": subjects,
        },
    )


def subject_detail(request, pk):
    subject = Subject.objects.get(pk=pk)

    return render(
        request,
        "tasks/subject_detail.html",
        {
            "title": f"Tema {subject.name}",
            "subject": subject,
        },
    )


def search(request):
    tasks = []
    query = ""
    if request.method == "POST":
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            tasks = Task.objects.filter(title__icontains=query)
            priority = form.cleaned_data.get("priority") or []
            if priority:
                tasks = tasks.filter(priority__in=priority)
            urgent = form.cleaned_data.get("urgent", False)
            if urgent:
                tasks = tasks.filter(urgent=True)
    else:
        form = forms.SearchForm()

    return render(
        request,
        "tasks/search.html",
        {
            "title": "Buscar tareas",
            "form": form,
            "tasks": tasks,
            "query": query,
        },
    )


def list_tasks_per_year(request, year):
    tasks = Task.objects.filter(created__year=year)
    return render(
        request,
        "tasks/list_tasks.html",
        {
            "title": f"Tareas creadas en el año {year}",
            "tasks": tasks,
        },
    )


def lab_view(request):
    return render(request, "tasks/lab.html", {"title": "Labs page,"})


def list_by_priority(request, priority):
    priority = priority[0].upper()
    tasks = Task.objects.filter(priority=priority)
    return render(
        request,
        "tasks/list_tasks.html",
        {
            "title": f"Tareas de prioridad {priority}",
            "tasks": tasks,
        },
    )


def create_task(request):
    if request.method == "POST":
        form = forms.CreateTaskForm(request.POST)
        if form.is_valid():
            new_task = form.save()
            return redirect("/")
    else:
        form = forms.CreateTaskForm()
    return render(
        request,
        "tasks/create_task.html",
        {
            "title": "Nueva Tarea",
            "form": form,
        },
    )


def edit_task(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == "POST":
        form = forms.EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return redirect("/")
    else:
        form = forms.EditTaskForm(instance=task)
    return render(
        request,
        "tasks/edit_task.html",
        {
            "title": f"Editar tarea #{task.pk}",
            "form": form,
        },
    )


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        task_id = serializer.instance.id

        response_data = {
            "status": {
                "type": "ok",
                "code": status.HTTP_200_OK,
                "message": "Task created successfully",
            },
            "id": task_id,
        }

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class TaskRetrieveView(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404:
            response_data = {
                "status": {
                    "type": "error",
                    "code": 404,
                    "message": "The requested task could not be found",
                }
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
