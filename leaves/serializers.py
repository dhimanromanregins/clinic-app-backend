from rest_framework import serializers
from .models import Leaves, SickLeaveRequestView, SickLeaveRecords,ToWhomItMayCocern,ParentSickLeave,ParentSickLeaveHistory

class LeavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = ['id', 'user', 'name', 'type', 'start_date', 'end_date', 'total_days', 'reason','approved']
        read_only_fields = ['total_days']


class SickLeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SickLeaveRequestView
        fields = ['id', 'children', 'to', 'sender']

class SickLeaveRecordsSerializer(serializers.ModelSerializer):
    document_url = serializers.SerializerMethodField()

    class Meta:
        model = SickLeaveRecords
        fields = ['id', 'children', 'document', 'leave_request_date', 'document_url']

    def get_document_url(self, obj):
        return f"http://192.168.1.111:8001{obj.document.url}"

class ParentSickLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentSickLeave
        fields = ['user', 'child_name', 'sent_to', 'sender']


class ParentSickLeaveHistorySerializer(serializers.ModelSerializer):
    document_url = serializers.SerializerMethodField()
    class Meta:
        model = ParentSickLeaveHistory
        fields = ['id', 'parent', 'document', 'created_date', 'leave_request_date', 'document_url']

    def get_document_url(self, obj):
        return f"http://192.168.1.111:8001{obj.document.url}"


class ToWhomItMayConcernSerializer(serializers.ModelSerializer):  # Fix the typo here
    class Meta:
        model = ToWhomItMayCocern  # Fix the model name here
        fields = ['id', 'concern', 'user', 'child_name', 'sent_to', 'sender', 'additional_notes']  # Fix the field names here