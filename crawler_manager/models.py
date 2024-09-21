from django.db import models


class CeleryControl(models.Model):
    name = models.CharField(max_length=100, default="Celery Control")

    def __str__(self):
        return self.name
