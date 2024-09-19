from django.db import models


class ParsedContent(models.Model):
    url = models.URLField(max_length=500)
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    headings = models.JSONField(blank=True, null=True)
    text = models.TextField(blank=True)
    links = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
