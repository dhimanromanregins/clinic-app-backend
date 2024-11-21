from rest_framework import serializers
from .models import Doctor, Location,Language, TeleDoctor,WorkingPeriod, DayOfWeek
from accounts.models import CustomUser


class DayOfWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayOfWeek
        fields = ['id', 'name']



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


class TeleDoctorSerializer(serializers.ModelSerializer):
    # Fields to be included in the response
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    parent_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = TeleDoctor
        fields = ['doctor_name', 'parent_name', 'doctor', 'user']

    def validate(self, attrs):
        # Ensure both doctor and user exist
        doctor_id = attrs.get('doctor')
        user_id = attrs.get('user')

        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("Doctor with this ID does not exist.")

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")

        return attrs


class WorkingPeriodSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()  # This will serialize the full doctor details
    day = serializers.CharField(source='day_of_week.name')  # Serialize the day name from the DayOfWeek model

    class Meta:
        model = WorkingPeriod
        fields = ['doctor', 'day', 'morning_start', 'morning_end', 'afternoon_start', 'afternoon_end']