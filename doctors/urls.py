from django.urls import path
from .views import * 
urlpatterns = [
       path('doctors/', DoctorListView.as_view(), name='doctors_list'),
       path('doctors/<int:doctor_id>/', DoctorDetailView.as_view(), name='doctor_detail'),
]

