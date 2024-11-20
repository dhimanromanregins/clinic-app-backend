
from django.http import JsonResponse
from .utils import generate_jwt_token,send_otp_in_background,send_otp_via_whatsapp
from .decorators import auth_check
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password
from datetime import datetime
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.views import APIView
from children.forms import ChildForm
from children.models import Child
from .models import CustomUser, Profile, Banner
from rest_framework.response import Response
from datetime import timedelta
from django.utils.decorators import method_decorator
from rest_framework import status
from django.views import View
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from datetime import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import CustomUserSerializer, BannerSerializer,OTPVerificationSerializer, LoginSerializer,ProfileSerializer


def send_otp(request):
    phone_number = request.POST.get('phone_number')
    otp = send_otp_in_background(phone_number)
    request.session['otp'] = otp

    return JsonResponse({'message': 'OTP sent successfully'})


# @csrf_exempt
# @auth_check
# def register(request):
#     if request.method == 'POST':
#         form = CustomUserRegistrationForm(request.POST)
#         if form.is_valid():
#             request.session['registration_data'] = form.cleaned_data
#             phone_number = form.cleaned_data['phone_number']
#             otp = send_otp_via_whatsapp(phone_number)
#             request.session['otp'] = otp

#             messages.success(request, f'OTP sent to {phone_number}. Please verify to complete registration.')
#             request.session['phone_number'] = phone_number
#             return redirect('verify_otp_login')
#     else:
#         form = CustomUserRegistrationForm()
#     return render(request, 'accounts/register.html', {'form': form})


class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        print(request.data)
        phone_number = request.data["phone_number"]
        id_number = request.data["id_number"]
        if CustomUser.objects.filter(phone_number=phone_number).exists():
                return Response(
                    {'message': 'This phone number is already registered.'},
                    status=status.HTTP_409_CONFLICT
                )
            
        if CustomUser.objects.filter(id_number=id_number).exists():
            return Response(
                {'message': 'This ID number is already registered.'},
                status=status.HTTP_409_CONFLICT
            )
        if serializer.is_valid():
            request.session['registration_data'] = serializer.validated_data
            registration_data = request.session.get('registration_data')
            print(registration_data, ')))))))))))))))))))')
            otp = send_otp_via_whatsapp(phone_number)
            request.session['otp'] = otp
            request.session['phone_number'] = phone_number
            print("121222222222222222222222222222222")
            return Response(
                {'message': f'OTP sent to {phone_number}. Please verify to complete registration.'},
                status=status.HTTP_201_CREATED
            )
        print("00000000000000000000000000000000000000000")
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpAPIView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        input_otp = request.data.get('otp')
        saved_otp = request.session.get('otp')

        if input_otp == str(saved_otp):
            registration_data = request.session.get('registration_data')
            if registration_data:
                serializer = CustomUserSerializer(data=registration_data)
                print(registration_data, '===============')

                if serializer.is_valid():
                    try:
                        user = CustomUser(
                            phone_number=serializer.validated_data['phone_number'],
                            id_number=serializer.validated_data['id_number'],
                            first_name=serializer.validated_data['first_name'],
                            last_name=serializer.validated_data['last_name']
                        )
                        # Use `set_password` to securely save the password
                        user.set_password(serializer.validated_data['password'])
                        user.save()

                        # Create the associated profile
                        Profile.objects.create(user=user)

                        # Generate JWT tokens
                        refresh = RefreshToken.for_user(user)
                        access_token = str(refresh.access_token)

                        # Clear session data after successful registration
                        request.session.pop('otp', None)
                        request.session.pop('registration_data', None)
                        request.session['user_id'] = user.id

                        return Response({
                            'status': status.HTTP_201_CREATED,
                            'message': 'Registration successful!',
                            'access_token': access_token,
                            'refresh_token': str(refresh)
                        }, status=status.HTTP_201_CREATED)

                    except IntegrityError:
                        return Response({
                            'error': 'A user with this phone number already exists. Please log in.'
                        }, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Registration data not found in session.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            password = serializer.validated_data.get('password')  # Get the password from request

            if not password:
                return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)

            user = None

            # Check if identifier is a phone number or an ID number
            if len(identifier) == 12:  # Phone number
                user = CustomUser.objects.filter(phone_number=identifier).first()
            elif len(identifier) == 18:  # ID number
                user = CustomUser.objects.filter(id_number=identifier).first()
            else:
                return Response({'error': 'Invalid identifier format.'}, status=status.HTTP_400_BAD_REQUEST)

            if user:  # User found
                # Use `check_password` to verify the hashed password
                if check_password(password, user.password):
                    phone_number = user.phone_number
                    otp = send_otp_via_whatsapp(phone_number)
                    request.session['otp'] = otp
                    request.session['phone_number'] = phone_number

                    return Response({
                        'phone_number': phone_number,
                        'status': True,
                        'message': f'OTP sent to {phone_number}. Please verify to complete login.'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class VerifyOtpLoginAPIView(APIView):
    def post(self, request):
        input_otp = request.data.get('otp')
        saved_otp = request.session.get('otp')
        phone_number = request.session.get('phone_number')
       
        if input_otp == str(saved_otp):
            
            user = authenticate(request, phone_number=phone_number)

            if user:
                auth_login(request, user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                messages.success(request, 'Logged in successfully!')
                
                return Response({
                    'status':status.HTTP_200_OK,
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'message': 'Logged in successfully!'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'User authentication failed.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'error': 'Invalid OTP'
            }, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(csrf_exempt, name='dispatch')
class ProfileListCreateView(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(csrf_exempt, name='dispatch')
class ProfileDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, request):
        try:
            return Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request):
        profile = self.get_object(request)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = self.get_object(request)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        print("Incoming data:", request.data)
        profile = self.get_object(request)
        data = request.data.copy()

        # Flatten the incoming data
        flattened_data = {key: value[0] if isinstance(value, list) and len(value) == 1 else value
                          for key, value in data.items()}

        # Handle profile picture
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']

            # Check if it's a valid file
            if hasattr(profile_picture, 'file') and profile_picture.size > 0:
                flattened_data['profile_picture'] = profile_picture
            else:
                # If it's not a valid file, remove 'profile_picture' from flattened_data
                print("Invalid file, profile picture will not be updated.")
                flattened_data.pop('profile_picture', None)  # Don't send it to the serializer

        # Validate and format date_of_birth if present
        if 'date_of_birth' in flattened_data:
            flattened_data['date_of_birth'] = flattened_data['date_of_birth'].strip()
            try:
                # Ensure the date format is correct
                datetime.strptime(flattened_data['date_of_birth'], '%Y-%m-%d')
            except ValueError:
                return Response(
                    {'date_of_birth': ['Invalid date format. Use YYYY-MM-DD.']},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Update the user fields (first_name, last_name) inside the request data if present
        user_data = {}
        if 'first_name' in flattened_data:
            user_data['first_name'] = flattened_data.pop('first_name')
        if 'last_name' in flattened_data:
            user_data['last_name'] = flattened_data.pop('last_name')
        if 'phone_number' in flattened_data:
            user_data['phone_number'] = flattened_data.pop('phone_number')
        if 'id_number' in flattened_data:
            user_data['id_number'] = flattened_data.pop('id_number')

        # If there is user data to update, update it on the user object
        if user_data:
            user = profile.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        # Debug the cleaned and flattened data
        print("Flattened data:", flattened_data)

        # Serialize the profile data
        serializer = ProfileSerializer(profile, data=flattened_data, partial=True)

        # Check if the serializer is valid
        if serializer.is_valid():
            serializer.save()

            # Custom response format after saving
            response_data = {
                'id': profile.id,
                'user': {
                    'first_name': profile.user.first_name,
                    'last_name': profile.user.last_name,
                    'id_number': profile.user.id_number,
                    'phone_number': profile.user.phone_number
                },
                'date_of_birth': profile.date_of_birth,
                'gender': profile.gender,
                'address': profile.address,
                'bio': profile.bio,
                'created_at': profile.created_at,
                'updated_at': profile.updated_at
            }

            print("Saved profile successfully.")
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            # If the serializer is not valid, return the errors
            print("Serializer validation failed:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, user_id):
        profile = self.get_object(user_id)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ForgotPasswordAPIView(APIView):
    permission_classes = []

    def post(self, request):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(phone_number=phone_number).first()

        if not user:
            return Response({'error': 'User with this phone number does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Generate OTP and send via WhatsApp
        otp = send_otp_via_whatsapp(phone_number)  # Use your OTP sending logic
        request.session['otp'] = otp
        request.session['phone_number'] = phone_number

        return Response({
            'status': True,
            'message': f'OTP sent to {phone_number}. Please verify to reset your password.'
        }, status=status.HTTP_200_OK)

class VerifyOtpForgotPasswordAPIView(APIView):
    def post(self, request):
        input_otp = request.data.get('otp')
        saved_otp = request.session.get('otp')
        phone_number = request.session.get('phone_number')

        if not input_otp or not phone_number:
            return Response({'error': 'OTP and phone number are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if input_otp == str(saved_otp):
            return Response({
                'status': True,
                'message': 'OTP verified. You can now reset your password.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(APIView):
    def post(self, request):
        phone_number = request.session.get('phone_number')
        new_password = request.data.get('new_password')

        if not phone_number or not new_password:
            return Response({'error': 'Phone number and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(phone_number=phone_number).first()

        if not user:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Update the password
        user.set_password(new_password)
        user.save()

        # Clear session data
        request.session.flush()

        return Response({
            'status': True,
            'message': 'Password reset successful.'
        }, status=status.HTTP_200_OK)

class BannerListView(APIView):
    """
    API View to get all banners.
    """
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)