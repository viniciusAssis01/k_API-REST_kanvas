from django.urls import path
from .views import ContentView, ContentDetailView

urlpatterns = [
    path("courses/<uuid:course_id>/contents/", ContentView.as_view()),
    path(
        "courses/<uuid:course_id>/contents/<uuid:content_id>/",
        ContentDetailView.as_view(),
    ),
]
