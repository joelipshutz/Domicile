import os
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from airtable import Airtable
import openai

#twilio
TWILIO_NUMBER = '+18442373707'
ACCOUNT_SID =  os.environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(ACCOUNT_SID, AUTH_TOKEN)

#airtable
AIRTABLE_BASE_ID = 'appG5fPUu0svngkio'
AIRTABLE_TABLE_NAME = 'tblHk3QzuDtwGTc2j'
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
airtable = Airtable('appG5fPUu0svngkio', 'tblHk3QzuDtwGTc2j', api_key=AIRTABLE_API_KEY)

#openAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

