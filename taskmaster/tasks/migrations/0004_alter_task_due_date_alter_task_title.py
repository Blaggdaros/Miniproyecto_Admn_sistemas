# Generated by Django 4.2.1 on 2023-05-12 15:57

from django.db import migrations, models

import tasks.models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0003_alter_task_due_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="due_date",
            field=models.DateField(
                blank=True,
                default=None,
                null=True,
                validators=[tasks.models.date_in_future],
                verbose_name="Fecha de entrega",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="title",
            field=models.CharField(max_length=250, unique=True, verbose_name="título"),
        ),
    ]
