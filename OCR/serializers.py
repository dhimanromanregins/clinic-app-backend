from rest_framework import serializers
from .models import UploadedPDF


class UploadedPDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedPDF
        fields = ['id', 'pdf_file', 'urn_number', 'category']
