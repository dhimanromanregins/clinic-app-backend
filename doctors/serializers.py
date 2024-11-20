from rest_framework import serializers
from .models import Doctor, Location,Language


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'city']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'language']


class DoctorSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    languages = LanguageSerializer(many=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'specialty', 'experience', 'about', 'hospital_name',
            'education', 'registration_id', 'profile_photo', 'digital_consult',
            'hospital_visit', 'price', 'is_available', 'location', 'languages'
        ]