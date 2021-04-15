from django.db import models
from project.models import Project


class Payment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payment')
    price = models.FloatField()
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.comment
