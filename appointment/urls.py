from django.urls import path
from .views import *


urlpatterns = [
    path('doctors/<int:doctor_id>/available_slots/', AvailableSlotsView.as_view(), name='available_slots'),
    path('api/bookings/', get_booked_slots, name='get_booked_slots'),
    path('book-slot/', BookSlotView.as_view(), name='book_slot'),
    path('api/user/bookings/', UserBookingListView.as_view(), name='user-bookings'),
    path('generatehashdata/', GenerateHashData.as_view(), name='generate_hash_data'),
]

