from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserConfirmation
import random

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number']

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, is_active=False)
        code = str(random.randint(100000, 999999))
        UserConfirmation.objects.create(user=user, code=code)
        print(f"Confirmation code for {user.email}: {code}")  # для теста
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("User is not active")
        data['user'] = user
        return data

class ConfirmUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        try:
            confirmation = user.confirmation
        except UserConfirmation.DoesNotExist:
            raise serializers.ValidationError("Confirmation code not found")
        if confirmation.code != data['code']:
            raise serializers.ValidationError("Incorrect confirmation code")
        data['user'] = user
        return data
