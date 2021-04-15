from django.db import models


class Client(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название компании')
    description = models.TextField()

    def __str__(self):
        return self.title

