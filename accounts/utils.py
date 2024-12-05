# utils.py

from twilio.rest import Client
from django.conf import settings
import requests
import random
import jwt
import datetime
import multiprocessing
import  json


def generate_otp():
    return random.randint(100000, 999999)


def send_otp_via_whatsapp(phone_number):
    print(phone_number, '-------------')
    otp = generate_otp()
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        messaging_service_sid=settings.MESSAGEING_SERVICE_SID,
        body=f'Your OTP is:{otp}',
        to=f'+{phone_number}'
    )
    print(message.sid)
    return otp

def send_otp_in_background(phone_number, request):
    otp_process = multiprocessing.Process(target=send_otp_via_whatsapp, args=(phone_number,))
    otp_process.start()
    otp_process.join()



def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def send_expo_push_notification(message):
    url = "https://exp.host/--/api/v2/push/send"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(message))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None





