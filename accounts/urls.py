from django.urls import path
from .views import  *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('update_user/', UpdateUserView.as_view(), name='update_user'),
    path('verify-otp/', VerifyOtpAPIView.as_view(), name='verify_otp'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify_otp_login/', VerifyOtpLoginAPIView.as_view(), name='verify_otp_login'),
    path('profiles/', ProfileListCreateView.as_view(), name='profile-list-create'),
    path('api/profile/', ProfileDetailView.as_view(), name='profile-detail'),
    # path('profile/create/', ProfileListCreateView.as_view(), name='create_profile'),
# Forgot Password
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('verify-forgot-password-otp/', VerifyOtpForgotPasswordAPIView.as_view(), name='verify_forgot_password_otp'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset_password'),
    path('api/banners/', BannerListView.as_view(), name='banner-list'),
    path('notifications/', UserNotificationsAPIView.as_view(), name='user-notifications'),
    path('notifications/<int:pk>/', NotificationUpdateAPIView.as_view(), name='update-notification'),
]

