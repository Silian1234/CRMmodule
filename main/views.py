# crm/views.py
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import UserSerializer, EventSerializer, EnrollmentStatusSerializer
from .models import CustomUser, Event, EnrollmentStatus
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.generics import RetrieveUpdateAPIView

class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: 'Пользователь успешно создан', 400: 'Ошибка валидации'}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Пользователь успешно создан",
                "token": token.key
            }, status=status.HTTP_201_CREATED)
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


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль'),
            }
        ),
        responses={200: 'Успешная авторизация', 400: 'Ошибка авторизации'}
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Успешная авторизация",
                "token": token.key
            }, status=status.HTTP_200_OK)
        return Response({"error": "Неверные учетные данные"}, status=status.HTTP_400_BAD_REQUEST)

class AddParticipantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        try:
            event.add_participant(request.user)
            return Response({"message": "Вы успешно добавлены к событию"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user