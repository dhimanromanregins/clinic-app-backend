from rest_framework import serializers
from .models import Leaves

class LeavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = ['id', 'user', 'name', 'type', 'start_date', 'end_date', 'total_days', 'reason','approved']
        read_only_fields = ['total_days']
