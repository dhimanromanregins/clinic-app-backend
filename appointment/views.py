from django.shortcuts import render
from doctors.models import Doctor
from django.shortcuts import get_object_or_404
from .models import Booking
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from rest_framework.views import APIView
from .serializers import BookingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class AvailableSlotsView(APIView):
    def get(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, id=doctor_id)
        selected_date_str = request.GET.get('selected_date', timezone.now().date())
        try:
            selected_date = timezone.datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        if selected_date < timezone.now().date():
            return Response({'error': 'Please choose the current or upcoming dates.'}, status=status.HTTP_400_BAD_REQUEST)
        day_of_week_str = selected_date.strftime('%A')
        weekly_slots = doctor.generate_weekly_slots()
        all_slots_for_day = weekly_slots.get(day_of_week_str, [])
        booked_slots = Booking.objects.filter(doctor=doctor, date=selected_date).values_list('slot_start', 'slot_end')
        available_slots = [
            {'start': slot[0].strftime('%H:%M:%S'), 'end': slot[1].strftime('%H:%M:%S')} for slot in all_slots_for_day if not any(
                start == slot[0] and end == slot[1] for start, end in booked_slots
            )
        ]
        return Response({'available_slots': available_slots, 'selected_date': selected_date_str}, status=status.HTTP_200_OK)


class BookSlotView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        print(request.data, '-------')
        if serializer.is_valid():
            # Create a booking
            serializer.save(user=request.user)
            return Response({'message': 'Slot booked successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_booked_slots(request):
    date = request.query_params.get('date')
    if not date:
        return Response({"error": "Date parameter is required"}, status=400)
    booked_slots = Booking.objects.filter(date=date)
    serializer = BookingSerializer(booked_slots, many=True)
    return Response(serializer.data)

class UserBookingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        bookings = Booking.objects.filter(user=user)

        # Prepare the response data
        response_data = []
        for booking in bookings:

            # Assuming booking has fields: slot_start, slot_end, date
            booking_data = {
                'id': booking.id,
                'slot_start': booking.slot_start,
                'slot_end': booking.slot_end,
                'date': booking.date,
                'doctor': {
                    'id':booking.doctor.id,
                    'name': booking.doctor.name,  # Assuming booking has a doctor field
                    'image': booking.doctor.profile_photo.url if booking.doctor.profile_photo else None,
                    "hospital_name":booking.doctor.hospital_name,
                    "price":booking.doctor.price,
                    "specialty":booking.doctor.specialty

                },
            }
            response_data.append(booking_data)

        return Response(response_data)


import hashlib
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status

class GenerateHashData(APIView):
    def post(self, request):
        try:
            # Get 'hash' data from the request body
            hash_data = request.data.get('hash', '')
            salt = "dWwGvm4Bv5bEsQpZWVtheoJIZyYgZ68W"
            data_to_hash = hash_data + salt

            # Generate SHA-512 hash
            hash_object = hashlib.sha512(data_to_hash.encode('utf-8'))
            generated_hash = hash_object.hexdigest()

            # Return the generated hash in a JSON response
            return Response({"hash": generated_hash}, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle errors and return appropriate response
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
