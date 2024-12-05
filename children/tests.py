from twilio.rest import Client

# Set your Account SID and Auth Token
account_sid = "AC520ddc60f52a78c3bc8b8b3e46ff2c03"
auth_token = "c6d2ce451bc7be9077c9bb90dd649603"
client = Client("AC520ddc60f52a78c3bc8b8b3e46ff2c03", "c6d2ce451bc7be9077c9bb90dd649603")

message = client.messages.create(
    from_="whatsapp:+552120420682",  # Your Twilio WhatsApp number
    to="whatsapp:+918894545979",  # The recipient's WhatsApp number
    body="Your appointment is coming up on July 21 at 3PM",  # Message content
)

print(message.body)
