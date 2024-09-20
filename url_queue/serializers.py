from rest_framework import serializers


class UrlQueueSerializer(serializers.Serializer):
    url = serializers.URLField()
