from rest_framework import serializers
from .models import Booking
from doctors.serializers import DoctorSerializer
from children.serializers import ChildSerializer



class SlotSerializer(serializers.Serializer):
    start = serializers.TimeField()
    end = serializers.TimeField()



class BookingSerializer(serializers.ModelSerializer):
    # doctor = DoctorSerializer()
    # child = ChildSerializer()

    class Meta:
        model = Booking
        fields = ['doctor', 'children_names', 'slot_start', 'slot_end', 'date', 'type']

        def validate(self, data):
            if Booking.objects.filter(
                doctor=data['doctor'],
                slot_start=data['slot_start'],
                slot_end=data['slot_end'],
                date=data['date']
            ).exists():
                raise serializers.ValidationError("Slot is already booked.")
            return data