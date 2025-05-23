from rest_framework import serializers
from ..models.user_model import User 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']  # Aaru thap aafai as needed
