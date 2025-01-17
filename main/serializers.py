from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(required=False)
    groups = serializers.SerializerMethodField()
    picture = serializers.ImageField(required=False, allow_null=True)

    def get_groups(self, obj):
        groups = obj.groups.all()
        if groups.exists():
            return groups.first().name
        return "Нет группы"
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            fatherName=validated_data.get('fatherName', ''),
            email=validated_data['email'],
            stack=validated_data.get('stack', ''),
            portfolio=validated_data.get('portfolio', ''),
            contacts=validated_data.get('contacts', ''),
            picture=validated_data.get('picture', None)
        )

        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'password', 'firstName', 'lastName', 'fatherName', 'email', 'stack', 'portfolio',
            'contacts', 'picture', 'groups'
        )
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class EventSerializer(serializers.ModelSerializer):
    leader = UserSerializer(read_only=True)
    curator = UserSerializer(read_only=True)
    leader_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(groups__name='leader'),
        source='leader',
        write_only=True,
        required=False,
        allow_null=True
    )
    curator_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(groups__name='curator'),
        source='curator',
        write_only=True,
        required=False,
        allow_null=True
    )
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = (
            'id', 'name', 'description', 'type', 'start_date', 'end_date',
            'enrollment_deadline', 'capacity', 'telegram_chat_link',
            'leader', 'curator', 'leader_id', 'curator_id', 'participants', 'picture', 'hidden'
        )

    def validate_leader(self, value):
        if value and not value.groups.filter(name="leader").exists():
            raise serializers.ValidationError("Выбранный пользователь не является лидером.")
        return value

    def validate_curator(self, value):
        if value and not value.groups.filter(name="curator").exists():
            raise serializers.ValidationError("Выбранный пользователь не является куратором.")
        return value

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


# В serializers.py
class EnrollmentStatusSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()

    class Meta:
        model = EnrollmentStatus
        fields = ('id', 'student', 'status', 'updated_at', 'student_id', 'event_id')

    def get_student(self, obj):
        student = obj.student
        # Возвращаем ФИО студента
        full_name = f"{student.lastName} {student.firstName}"
        if student.fatherName:
            full_name += f" {student.fatherName}"
        return full_name


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'created_at', 'is_read']
