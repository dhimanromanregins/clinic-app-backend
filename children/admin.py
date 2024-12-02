from django.contrib import admin
from .models import Child, Documents


class ChildAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('full_name', 'child_id_number', 'UAE_number', 'gender', 'relation', 'date_of_birth', 'grade')

    # Enable search functionality for these fields
    search_fields = ('child_id_number', 'UAE_number', 'full_name')

    # Add filters for easier navigation
    list_filter = ('gender', 'relation', 'grade', 'nationality')


# Register models with the customized admin class
admin.site.register(Child, ChildAdmin)
class DocumentsAdmin(admin.ModelAdmin):
    # Add filters for category and child
    list_filter = ('category', 'child')

    # Optionally, add columns to display in the list view
    list_display = ('child', 'Name', 'category', 'document')

    # You can also add search fields if needed
    search_fields = ('Name', 'category', 'child__name')  # Adjust based on how 'Child' is represented

    # Optionally, you can define list ordering
    ordering = ('child', 'category')

# Register the model with the custom admin class
admin.site.register(Documents, DocumentsAdmin)
