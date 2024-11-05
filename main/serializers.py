
from rest_framework import serializers
from .models import CustomUser

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
            role=validated_data['role'],
            picture=validated_data.get('picture', None)
        )
        return user

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'firstName', 'lastName', 'fatherName', 'email', 'stack', 'portfolio', 'contacts', 'role', 'picture')
