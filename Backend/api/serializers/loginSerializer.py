from rest_framework import serializers
from ..models.user_model import User

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        user = User.objects.filter(email=email).first()
        print(user.check_password(password))
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        return data
