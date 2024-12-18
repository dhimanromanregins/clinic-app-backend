from twilio.rest import Client
from django.conf import settings
import requests
import random
import jwt
import datetime
import multiprocessing
import  json



def send_notification_via_whatsapp(phone_number, user_name):
    print(phone_number, '-------------', user_name)
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    message_sid = settings.MESSAGING_SERVICE_SID
    content_sid = settings.NOTIFICATION_CONTENT_SID
    from_number = settings.TWILIO_WHATSAPP_FROM
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        content_sid=content_sid,
        to=f"whatsapp:+{phone_number}",
        from_=from_number,
        content_variables=json.dumps({"1": user_name}),
        messaging_service_sid=message_sid,
    )
    print(message.sid)
    return user_name