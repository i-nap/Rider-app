from rest_framework import serializers
from ..models.group_model import Group  
from .user_serializer import  UserSerializer

class GroupSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'admin',
            'start_latitude',
            'start_longitude',
            'dest_latitude',
            'dest_longitude',
            'start_date',
            'expected_end_date',
            'member_count',
            'created_at',
            'updated_at',
            'private',
        ]
