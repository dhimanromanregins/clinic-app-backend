from django.urls import path
from .views import  *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOtpAPIView.as_view(), name='verify_otp'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify_otp_login/', VerifyOtpLoginAPIView.as_view(), name='verify_otp_login'),
    path('profiles/', ProfileListCreateView.as_view(), name='profile-list-create'),
    path('api/profile/', ProfileDetailView.as_view(), name='profile-detail'),
    # path('profile/create/', ProfileListCreateView.as_view(), name='create_profile'),
]

