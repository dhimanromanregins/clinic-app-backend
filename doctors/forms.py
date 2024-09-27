from django import forms
from .models import Doctor, WorkingPeriod, DayOfWeek


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialty', 'location', 'experience', 'about', 'hospital_name',
                  'education', 'registration_id', 'profile_photo', 'digital_consult',
                  'hospital_visit', 'price', 'is_available', 'languages']


class WorkingPeriodForm(forms.ModelForm):
    class Meta:
        model = WorkingPeriod
        fields = ['doctor', 'day_of_week', 'morning_start', 'morning_end', 'afternoon_start', 'afternoon_end']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally customize fields if needed, e.g., add widgets or filter choices
        self.fields['morning_start'].widget = forms.TimeInput(attrs={'type': 'time'})
        self.fields['morning_end'].widget = forms.TimeInput(attrs={'type': 'time'})
        self.fields['afternoon_start'].widget = forms.TimeInput(attrs={'type': 'time'})
        self.fields['afternoon_end'].widget = forms.TimeInput(attrs={'type': 'time'})



