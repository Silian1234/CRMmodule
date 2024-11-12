from django.urls import path
from .views import (
    RegisterView, EventListCreateView, EventDetailView, EnrollmentStatusListCreateView, EnrollmentStatusDetailView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('enrollment-status/', EnrollmentStatusListCreateView.as_view(), name='enrollment-status-list-create'),
    path('enrollment-status/<int:pk>/', EnrollmentStatusDetailView.as_view(), name='enrollment-status-detail'),
]