from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'body',
            'is_completed',
            'created_at',
            'updated_at',
            'owner'
        )