from django.contrib import admin
from .models import UploadedPDF

@admin.register(UploadedPDF)
class UploadedPDFAdmin(admin.ModelAdmin):
    # Add filters for category and urn_number
    list_filter = ('category', 'urn_number')

    # Columns to display in the list view
    list_display = ('pdf_file', 'urn_number', 'category')

    # Enable search functionality on pdf_file name, urn_number, and category
    search_fields = ('pdf_file__name', 'urn_number', 'category')

    # Set default ordering (optional)
    ordering = ('category', 'urn_number')
