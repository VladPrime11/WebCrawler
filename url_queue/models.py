from django.db import models


class UrlQueue(models.Model):
    url = models.URLField(max_length=500)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return self.url
