from django.contrib import admin
from .models import Doctor, Location, DayOfWeek, WorkingPeriod, Language, TeleDoctor
from .forms import DoctorForm


class DoctorsAdmin(admin.ModelAdmin):
    form = DoctorForm
    list_display = ('name', 'specialty', 'is_available', 'tele_medicine_doctor')
    search_fields = ('name', 'specialty', 'hospital_name')
    list_filter = ('is_available', 'tele_medicine_doctor', 'location')

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
admin.site.register(WorkingPeriod)
admin.site.register(Language)
admin.site.register(TeleDoctor)
