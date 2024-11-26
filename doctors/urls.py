from django.urls import path
from .views import *

urlpatterns = [
       path('doctors/', DoctorListView.as_view(), name='doctors_list'),
       path('doctors/<int:doctor_id>/', DoctorDetailView.as_view(), name='doctor_detail'),
       path('create-tele-doctor/', CreateTeleDoctorAPIView.as_view(), name='create_tele_doctor'),
       path('api/doctors-availability/', DoctorAvailabilityAPIView.as_view(), name='doctor-availability'),
       path('api/available-telemedicine-doctors/', AvailableTeleMedicineDoctorsView.as_view(), name='available-telemedicine-doctors'),
]

