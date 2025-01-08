# crm/views.py
from django.db.models import Q
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.parsers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import UserSerializer, EventSerializer, EnrollmentStatusSerializer, NotificationSerializer
from .models import CustomUser, Event, EnrollmentStatus, Notification
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, UpdateAPIView
from CRMmodule.authentication import *
from rest_framework.permissions import DjangoModelPermissions

class RegisterView(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, description='Имя пользователя', type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('password', openapi.IN_FORM, description='Пароль', type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('firstName', openapi.IN_FORM, description='Имя', type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('lastName', openapi.IN_FORM, description='Фамилия', type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('fatherName', openapi.IN_FORM, description='Отчество', type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('email', openapi.IN_FORM, description='Email', type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('stack', openapi.IN_FORM, description='Стэк', type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('portfolio', openapi.IN_FORM, description='Портфолио', type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('contacts', openapi.IN_FORM, description='Контакты', type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('picture', openapi.IN_FORM, description='Фото', type=openapi.TYPE_FILE, required=False),
        ],
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
    parser_classes = [MultiPartParser]
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [DjangoModelPermissions]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        return Event.objects.filter(hidden=False)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [BearerTokenAuthentication]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [DjangoModelPermissions]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        return Event.objects.filter(hidden=False)

class EnrollmentStatusListCreateView(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [BearerTokenAuthentication]
    queryset = EnrollmentStatus.objects.all()
    serializer_class = EnrollmentStatusSerializer
    permission_classes = [DjangoModelPermissions]

class EnrollmentStatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [BearerTokenAuthentication]
    queryset = EnrollmentStatus.objects.all()
    serializer_class = EnrollmentStatusSerializer
    permission_classes = [DjangoModelPermissions]


class LoginView(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, description='Имя пользователя', type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('password', openapi.IN_FORM, description='Пароль', type=openapi.TYPE_STRING, required=True),
        ],
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
    parser_classes = [MultiPartParser]
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        if timezone.now() > event.enrollment_deadline:
            return Response(
                {"error": "Дедлайн регистрации на это мероприятие уже прошёл"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            event.add_participant(request.user)
            return Response({"message": "Вы успешно добавлены к событию"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(RetrieveUpdateAPIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UserProfileView(RetrieveUpdateAPIView):
    parser_classes = [MultiPartParser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class LeaderCuratorListView(ListAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = UserSerializer
    def get_queryset(self):
        return CustomUser.objects.filter(Q(groups__name='leader') | Q(groups__name='curator'))

class NotificationListView(ListAPIView):
    authentication_classes = [BearerTokenAuthentication]
    parser_classes = [MultiPartParser]
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class MarkNotificationReadView(UpdateAPIView):
    authentication_classes = [BearerTokenAuthentication]
    parser_classes = [MultiPartParser]
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False)

    def perform_update(self, serializer):
        serializer.instance.is_read = True
        serializer.save()

class DataSubmittedStudentsForEventView(ListAPIView):
    authentication_classes = [BearerTokenAuthentication]
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        statuses = EnrollmentStatus.objects.filter(event_id=event_id, status='data_submitted')
        student_ids = statuses.values_list('student_id', flat=True)
        return CustomUser.objects.filter(id__in=student_ids)

class EnrollmentStatusFilteredListView(ListAPIView):
    authentication_classes = [BearerTokenAuthentication]
    serializer_class = EnrollmentStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = EnrollmentStatus.objects.all()
        user_id = self.kwargs.get('user_id')
        event_id = self.kwargs.get('event_id')

        if user_id:
            queryset = queryset.filter(student_id=user_id)
        if event_id:
            queryset = queryset.filter(event_id=event_id)

        return queryset

class RemoveStudentFromEventView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, event_id, student_id):
        try:
            event = Event.objects.get(id=event_id)
            student = CustomUser.objects.get(id=student_id)
        except (Event.DoesNotExist, CustomUser.DoesNotExist):
            return Response({"error": "Мероприятие или студент не найдены"}, status=404)

        event.participants.remove(student)
        EnrollmentStatus.objects.create(student=student, event=event, status='removed')
        return Response({"message": "Студент удалён с мероприятия"}, status=200)