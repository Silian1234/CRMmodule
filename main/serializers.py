from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import CustomUser, Event, EnrollmentStatus


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

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


class EventSerializer(serializers.ModelSerializer):
    leader = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(groups__name="leader"),
        required=False,
        allow_null=True
    )
    curator = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(groups__name="curator"),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'type', 'start_date', 'end_date',
                  'enrollment_deadline', 'capacity', 'telegram_chat_link', 'leader', 'curator')

    def validate_leader(self, value):
        if value and not value.groups.filter(name="leader").exists():
            raise serializers.ValidationError("Выбранный пользователь не является лидером.")
        return value

    def validate_curator(self, value):
        if value and not value.groups.filter(name="curator").exists():
            raise serializers.ValidationError("Выбранный пользователь не является куратором.")
        return value

class EnrollmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentStatus
        fields = ('id', 'student', 'event', 'status', 'updated_at')
