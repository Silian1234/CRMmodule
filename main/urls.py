from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('enrollment-status/', EnrollmentStatusListCreateView.as_view(), name='enrollment-status-list-create'),
    path('enrollment-status/<int:pk>/', EnrollmentStatusDetailView.as_view(), name='enrollment-status-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/me/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('events/<int:event_id>/add-participant/', AddParticipantView.as_view(), name='add-participant'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/edit/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('leader-curator/', LeaderCuratorListView.as_view(), name='leader-curator'),
]