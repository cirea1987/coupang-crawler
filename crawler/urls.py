from django.urls import path
from .views import CrawlerView

urlpatterns = [
    path('', CrawlerView.as_view())
]
