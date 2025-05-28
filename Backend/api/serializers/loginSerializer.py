from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password_hash = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password_hash')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        from ..models.user_model import User
        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        return data
