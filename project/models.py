from django.db import models
from client.models import Client
from django.contrib.auth.models import User


class Project(models.Model):
    STATUS_CHOICES = [
        ('p', 'Planned'),
        ('i', 'In_progress'),
        ('t', 'Testing'),
        ('r', 'Release'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='project')
    title = models.CharField(max_length=50, verbose_name='Название проекта')
    description = models.TextField()
    start_date = models.DateField(verbose_name='Начало проекта')
    release_date = models.DateField(verbose_name='Конец проекта')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title


class Task(models.Model):
    STATUS_CHOICES = [
        ('t', 'To_do'),
        ('i', 'In_progress'),
        ('t', 'Testing'),
        ('d', 'Done'),
    ]

    TYPE_CHOICES = [
        ('p', 'Programming'),
        ('y', 'Deploy'),
        ('t', 'Testing'),
        ('d', 'Design'),
        ('l', 'Layout'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='task')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task', verbose_name='Кто выполняет задачу')
    title = models.CharField(max_length=50, verbose_name='Название задачи')
    description = models.TextField()
    start_datetime = models.DateTimeField(verbose_name='Начало выполнения задачи')
    release_datetime = models.DateTimeField(verbose_name='Конец выполнения задачи')
    total_time = models.FloatField(verbose_name='Общее время выполнения задачи в часах')
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title


class CommentTask(models.Model):
    STATUS_CHOICES = [
        ('t', 'To_do'),
        ('i', 'In_progress'),
        ('t', 'Testing'),
        ('d', 'Done'),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comment_task')
    user = models.CharField(max_length=50)
    comment = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    time = models.FloatField(verbose_name='Время выполнения задачи в часах')

    def __str__(self):
        return self.user


# class Image(models.Model):
#     pass





