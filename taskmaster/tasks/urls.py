from django.urls import path

from .views import TaskListCreateView, TaskRetrieveView

urlpatterns = [
    # Otras rutas existentes...
    path("api/tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("api/tasks/<int:pk>/", TaskRetrieveView.as_view(), name="task-retrieve"),
]
