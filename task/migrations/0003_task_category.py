# Generated by Django 5.1.3 on 2024-12-19 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_task_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.CharField(choices=[('Work', 'Work'), ('Personal', 'Personal'), ('Other', 'Other')], default='Other', max_length=20),
        ),
    ]
