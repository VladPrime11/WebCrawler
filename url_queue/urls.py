from django.urls import path
from .views import add_url_view

urlpatterns = [
    path('add-url/', add_url_view, name='add_url'),
]
