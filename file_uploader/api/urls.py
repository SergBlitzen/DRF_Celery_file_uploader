from django.urls import path

from api.views import FileCreateView, FileListView


urlpatterns = [
    path('v1/upload/', FileCreateView.as_view()),
    path('v1/files/', FileListView.as_view()),
]
