from django import forms
from .models import Appointment, Booking
from doctors.models import Doctor

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_time']
        widgets = {
            'appointment_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['doctor', 'date', 'slot_start', 'slot_end']

    def __init__(self, *args, **kwargs):
        # Allow passing the selected date and doctor as initial data
        selected_date = kwargs.pop('selected_date', None)
        doctor_id = kwargs.pop('doctor_id', None)
        super().__init__(*args, **kwargs)

        # If doctor ID is provided, filter slot choices based on that doctor
        if doctor_id:
            self.fields['doctor'].queryset = Doctor.objects.filter(id=doctor_id)

        # Set initial date if provided
        if selected_date:
            self.fields['date'].initial = selected_date

        # Optionally, set custom widgets or field attributes here
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['slot_start'].widget = forms.TimeInput(attrs={'type': 'time'})
        self.fields['slot_end'].widget = forms.TimeInput(attrs={'type': 'time'})