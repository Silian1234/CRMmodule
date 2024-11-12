# crm/views.py
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import UserSerializer, EventSerializer, EnrollmentStatusSerializer
from .models import CustomUser, Event, EnrollmentStatus
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Регистрация пользователя
class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: 'Пользователь успешно создан', 400: 'Ошибка валидации'}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь успешно создан"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class EnrollmentStatusListCreateView(generics.ListCreateAPIView):
    queryset = EnrollmentStatus.objects.all()
    serializer_class = EnrollmentStatusSerializer
    permission_classes = [IsAdminUser]

class EnrollmentStatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EnrollmentStatus.objects.all()
    serializer_class = EnrollmentStatusSerializer
    permission_classes = [IsAdminUser]
