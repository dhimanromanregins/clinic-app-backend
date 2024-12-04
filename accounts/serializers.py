from rest_framework import serializers
from .models import CustomUser, Profile, Banner, Notifications


class CustomUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'id_number','password', 'device_token']


    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def validate_phone_number(self, phone_number):
        print(phone_number, 'Processing phone number validation.')
        # Ensure the phone number contains only digits
        if not phone_number.isdigit():
            raise serializers.ValidationError('Phone number must contain only digits.')

        # Check if the phone number starts with '91' and add it if not
        if not phone_number.startswith('971'):
            phone_number = '971' + phone_number

        # Validate length: Country code (2) + 10 digits = 12
        if len(phone_number) != 13:
            raise serializers.ValidationError('Phone number must be 10 digits long, excluding the country code.')

        # Check if the phone number already exists in the database
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError('Phone number already exists. Try logging in.')
        return phone_number

    def validate_id_number(self, id_number):
        # Check if the id_number already exists in the database
        if CustomUser.objects.filter(id_number=id_number).exists():
            raise serializers.ValidationError('ID number already exists. Try logging in.')
        return id_number

class OTPVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, required=True)

    def validate(self, data):
        input_otp = data['otp']
        saved_otp = self.context['request'].session.get('otp')

        if input_otp != str(saved_otp):
            raise serializers.ValidationError('Invalid OTP.')

        return data

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=18)  # 12 for phone, 18 for ID
    password = serializers.CharField(write_only=True)

    def validate_identifier(self, value):
        if len(value) != 13 and len(value) != 8:
            raise serializers.ValidationError("Identifier must be either 13 (phone) or 18 (ID) characters long.")
        return value


class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()  # Nested CustomUserSerializer to handle user data

    class Meta:
        model = Profile
        fields = '__all__'

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                if value is not None:
                    setattr(user, attr, value)

            user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance



class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['id', 'title', 'body', 'is_read']
