from twilio.rest import Client

account_sid = 'AC46c5fb2956bc83ed407e4f1bc567e934'
auth_token = '5628bfce9dea96c114e2ef60590a6030'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='Your appointment is coming up on July 21 at 3PM',
  to='whatsapp:+916367006928'
)

print(message.sid)