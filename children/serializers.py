from rest_framework import serializers
from .models import Child, Documents, Vaccination

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'


class DocumentsSerializer(serializers.ModelSerializer):
    document_url = serializers.SerializerMethodField()
    class Meta:
        model = Documents
        fields = fields = ['id', 'child', 'parent','document', 'Name', 'document_url']

    def get_document_url(self, obj):
        return f"http://192.168.1.111:8001{obj.document.url}"


class VaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = '__all__'