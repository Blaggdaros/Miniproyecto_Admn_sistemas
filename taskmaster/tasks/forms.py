from django import forms

from tasks.models import Task

PRIORITIES = [
    ("L", "Prioridad baja"),
    ("N", "Prioridad normal"),
    ("H", "Prioridad alta"),
]


class SearchForm(forms.Form):
    query = forms.CharField(label="Buscar")
    priority = forms.MultipleChoiceField(
        label="Prioridad",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=PRIORITIES,
    )
    urgent = forms.BooleanField(
        required=False,
        label="Urgente",
    )


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "subject", "due_date", "priority", "urgent"]


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "subject", "due_date", "priority", "urgent"]
