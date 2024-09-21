from django.urls import path
from .views import add_url_view, start_crawler
from . import views

urlpatterns = [
    path('add-url/', add_url_view, name='add_url'),
    path('clear-queue/', views.clear_queue_view, name="clear_queue"),
    path('start-crawler/', start_crawler, name='start_crawler'),
]
