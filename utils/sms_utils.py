from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from config import TWILIO_NUMBER, ACCOUNT_SID, AUTH_TOKEN, client
from utils.logs import convos_log

def send_sms(to_number, body):
    print(f"Outgoing message to {to_number}: {body}")  # Log outgoing messages
    convos_log.append(f"Outgoing message to {to_number}: {body}")  # Add to the conversation log
    client.messages.create(
        body=body,
        from_=TWILIO_NUMBER,
        to=to_number
    )
