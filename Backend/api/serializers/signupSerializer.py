from rest_framework import serializers
from ..models.user_model import User

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'password_hash']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already in use.")
        return value