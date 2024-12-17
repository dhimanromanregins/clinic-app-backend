import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'user', 'patient_arrived', 'slot_start', 'slot_end', 'date')
    list_filter = ('patient_arrived',)  # Filter for patient_arrived field
    search_fields = ('doctor__name', 'user__username')  # Optional: Add search functionality
    ordering = ('date',)  # Optional: Order by date

    actions = ['export_all_bookings_to_csv']

    def export_all_bookings_to_csv(self, request, queryset):
        """
        Export all bookings to a CSV file.
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="all_bookings.csv"'

        writer = csv.writer(response)
        writer.writerow(['Doctor', 'User', 'Patient Arrived', 'Slot Start', 'Slot End', 'Date'])

        for booking in queryset:
            writer.writerow([
                booking.doctor.name,
                booking.user.first_name,
                booking.patient_arrived,
                booking.slot_start,
                booking.slot_end,
                booking.date
            ])

        return response

    export_all_bookings_to_csv.short_description = "Export All Bookings to CSV"
