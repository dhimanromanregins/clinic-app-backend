
from django.shortcuts import render, get_object_or_404

from rest_framework import status

from datetime import datetime
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Doctor, Location, Language, DayOfWeek,TeleDoctor,WorkingPeriod
from accounts.models import CustomUser
from .serializers import DoctorSerializer,TeleDoctorSerializer, WorkingPeriodSerializer
import time

class DoctorListView(APIView):
    def get(self, request):
        # Retrieve all locations and languages
        locations = Location.objects.all()
        languages = Language.objects.all()
        
        # Get query parameters
        selected_location_name = request.GET.get('location')
        selected_language_names = request.GET.getlist('languages')
        selected_consult_modes = request.GET.getlist('consult_modes')
        selected_fees = request.GET.getlist('fees')
        search_query = request.GET.get('search', '')

        # Initialize the queryset
        doctors = Doctor.objects.all()

        # Map names to IDs for filtering
        location_map = {location.city: location.id for location in locations}
        language_map = {language.language: language.id for language in languages}

        # Convert names to IDs
        selected_location_id = location_map.get(selected_location_name)
        selected_language_ids = [language_map.get(name) for name in selected_language_names]

        if selected_location_id:
            doctors = doctors.filter(location_id=selected_location_id)

        if search_query:
            doctors = doctors.filter(
                Q(name__icontains=search_query) |
                Q(registration_id__icontains=search_query)
            )

        if selected_language_ids:
            doctors = doctors.filter(languages__in=selected_language_ids).distinct()

        if selected_consult_modes:
            if 'Hospital Visit' in selected_consult_modes:
                doctors = doctors.filter(hospital_visit=True)
            if 'Online Consult' in selected_consult_modes:
                doctors = doctors.filter(digital_consult=True)

        if selected_fees:
            fee_ranges = {
                '100-500': (100, 500),
                '500-1000': (500, 1000),
                '1000+': (1000, None)
            }
            filters = Q()
            for fee in selected_fees:
                if fee in fee_ranges:
                    min_price, max_price = fee_ranges[fee]
                    if max_price:
                        filters |= Q(price__gte=min_price, price__lte=max_price)
                    else:
                        filters |= Q(price__gte=min_price)
            doctors = doctors.filter(filters)

        serializer = DoctorSerializer(doctors, many=True)

        location_names = [location.city for location in locations]
        language_names = [language.language for language in languages]

        return Response({
            'doctors': serializer.data,
            'locations': location_names,
            'languages': language_names,
            'doctors_count': doctors.count(),
            'selected_location': selected_location_name if selected_location_name in location_names else '',
            'selected_languages': [name for name in selected_language_names if name in language_names],
            'selected_consult_modes': selected_consult_modes,
            'selected_fees': selected_fees
        })




class DoctorDetailView(APIView):
    def get(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, id=doctor_id)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTeleDoctorAPIView(APIView):
    # Ensure that the user is authenticated
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doctor_id = request.data.get('doctor_id')

        # Get the user_id from the authenticated user
        user_id = request.user.id  # This will give you the user ID of the authenticated user

        print(request.data, "99999999999999999", doctor_id, user_id)

        if not doctor_id or not user_id:
            return Response({'error': 'doctor_id and user_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the doctor using the doctor_id
            doctor = Doctor.objects.get(id=doctor_id)

            # Get the user using the user_id (this comes from the request.user)
            user = CustomUser.objects.get(id=user_id)

            # Create TeleDoctor instance
            tele_doctor = TeleDoctor.objects.create(doctor=doctor, user=user)

            # Serialize the TeleDoctor instance
            serializer = TeleDoctorSerializer(tele_doctor)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class DoctorAvailabilityAPIView(APIView):
    def get(self, request, *args, **kwargs):
        date_str = request.query_params.get('date')  # Get the date from query params
        if not date_str:
            return Response({"error": "Date is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')  # Parse the date
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the day of the week (0 = Monday, 6 = Sunday)
        day_of_week = date_obj.weekday() + 1  # Adjust for 1-indexed DayOfWeek model

        # Filter WorkingPeriods for the given day
        working_periods = WorkingPeriod.objects.filter(day_of_week__id=day_of_week)

        # Serialize the filtered data
        serializer = WorkingPeriodSerializer(working_periods, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class AvailableTeleMedicineDoctorsView(APIView):
    def get(self, request):
        doctors = Doctor.objects.filter(tele_medicine_doctor=True)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)