# utils.py

from twilio.rest import Client
from django.conf import settings
import random
import jwt
import datetime
import multiprocessing


def generate_otp():
    return random.randint(100000, 999999)


def send_otp_via_whatsapp(phone_number):
    print(phone_number, '-------------')
    otp = generate_otp()
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_='whatsapp:+14155238886',
        to=f'whatsapp:{phone_number}'
    )
    print(message.sid)
    print(otp, "+++++++++++++++++")
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



