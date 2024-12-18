from django.contrib import admin
from .models import Doctor, Location, DayOfWeek, WorkingPeriod, Language, TeleDoctor
from .forms import DoctorForm


class DoctorsAdmin(admin.ModelAdmin):
    form = DoctorForm
    list_display = ('name', 'specialty', 'is_available', 'tele_medicine_doctor')
    search_fields = ('name', 'specialty', 'hospital_name', 'phone_number')
    list_filter = ('is_available', 'tele_medicine_doctor', 'location', 'phone_number')

    def display_languages(self, obj):
        return ", ".join([language.language for language in obj.languages.all()])

    display_languages.short_description = 'Languages'

    def display_working_days(self, obj):
        # Get the working periods for this doctor
        working_periods = WorkingPeriod.objects.filter(doctor=obj)
        # Extract the days from the working periods
        days = [wp.day_of_week.name for wp in working_periods]
        return ', '.join(days) if days else 'Not specified'

    display_working_days.short_description = 'Working Days'


# Register the models and admin classes
admin.site.register(Doctor, DoctorsAdmin)
admin.site.register(Location)
admin.site.register(DayOfWeek)
class WorkingPeriodAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = (
        'doctor', 'day_of_week',
        'morning_start', 'morning_end',
        'afternoon_start', 'afternoon_end'
    )

    # Enable filtering in the admin sidebar
    list_filter = (
        'doctor', 'day_of_week',
        'morning_start', 'morning_end',
        'afternoon_start', 'afternoon_end',
    )

    # Enable searching for doctors by their name
    search_fields = ('doctor__name',)  # Assuming Doctor model has a 'name' field

    # Optional: Ordering of records in the admin list view
    ordering = ('doctor', 'day_of_week')

# Register the WorkingPeriod model with the customized admin class
admin.site.register(WorkingPeriod, WorkingPeriodAdmin)
admin.site.register(Language)
admin.site.register(TeleDoctor)
