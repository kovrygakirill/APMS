from django.db import models


class Client(models.Model):
    title = models.CharField(max_length=50, verbose_name='Name of company')
    description = models.TextField()

    def get_description(self):
        return self.description[:30] + " ..." if len(self.description) >= 30 else self.description

    get_description.short_description = 'description'

    def __str__(self):
        return self.title

