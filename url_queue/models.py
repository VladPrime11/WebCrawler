from django.db import models


class UrlQueue(models.Model):
    url = models.URLField(max_length=1000)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return self.url
