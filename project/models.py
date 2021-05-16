from django.db import models
from client.models import Client
from user_profile.models import UserProfile


class Project(models.Model):
    STATUS_CHOICES = [
        ('p', 'Planned'),
        ('d', 'Doing'),
        ('t', 'Testing'),
        ('r', 'Release'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='project')
    title = models.CharField(max_length=50, verbose_name='Name of project')
    description = models.TextField()
    start_date = models.DateField(verbose_name='Start')
    release_date = models.DateField(verbose_name='Finish')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def get_description(self):
        return self.description[:10] + " ..." if len(self.description) >= 30 else self.description

    get_description.short_description = 'description'

    def __str__(self):
        return self.title


class Task(models.Model):
    STATUS_CHOICES = [
        ('o', 'Do'),
        ('i', 'Doing'),
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
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='task', verbose_name='Appointed by')
    title = models.CharField(max_length=50, verbose_name='Name of task')
    description = models.TextField()
    start_datetime = models.DateTimeField(verbose_name='Start task')
    release_datetime = models.DateTimeField(verbose_name='Finish task')
    total_time = models.FloatField(verbose_name='Total time complete')
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def get_description(self):
        return self.description[:30] + " ..." if len(self.description) >= 30 else self.description

    get_description.short_description = 'description'

    def __str__(self):
        return self.title


class CommentTask(models.Model):
    STATUS_CHOICES = [
        ('o', 'Do'),
        ('i', 'Doing'),
        ('t', 'Testing'),
        ('d', 'Done'),
    ]
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comment_task')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comment_task', verbose_name='Appointed by')
    comment = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    time = models.FloatField(verbose_name='Time complete')

    def save(self, *args, **kwargs):
        self.task.status = self.status
        self.task.user = self.user
        self.task.total_time += self.time
        self.task.save()
        super(CommentTask, self).save(*args, **kwargs)

    def get_comment(self):
        return self.comment[:30] + " ..." if len(self.comment) >= 30 else self.comment

    get_comment.short_description = 'comment'

    def __str__(self):
        return self.get_comment()


# class Image(models.Model):
#     pass





