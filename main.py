from airtable import Airtable
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import time
import datetime
import os
import openai
from utils.logs import convos_log

from questions import questions
from utils.openai_utils import format_conversation, check_photographer_response, get_photography_times
from utils.airtable_utils import get_records, update_record
from utils.sms_utils import send_sms
from utils.validation_utils import is_address_valid


app = Flask(__name__)

conversations = {}

def get_next_question(from_number):
    conversation = conversations[from_number]
    for question in questions:
        if question['field'] not in conversation:
            # if there are conditions for this question
            if 'conditions' in question:
                # all conditions must be true
                if not all([conversation.get(condition['field'], {}).get('response').lower() == condition['response'] for condition in question['conditions']]):
                    continue

            return question
    return None


@app.route('/sms', methods=['POST'])
def sms_reply():
    from_number = request.values.get('From')
    body = request.values.get('Body')

    print(f"Incoming message from {from_number}: {body}")  # Log incoming messages
    convos_log.append(f"Incoming message from {from_number}: {body}")  # Add to the conversation log

    if from_number not in conversations:
        print(f"New conversation started with {from_number}")  # Debug: New conversation started
        conversations[from_number] = {}

    last_question = get_next_question(from_number)
    # Check if this number is a photographer currently being asked to schedule a time
    if 'scheduling' in conversations[from_number] and conversations[from_number]['scheduling']:
    # Check to see if the photographer replied with a valid date-time
        next_message = check_photographer_response(body, conversations[from_number])
        if valid_datetime:
            # The photographer has replied with a time
            confirmed_time = response

            # Update the record in Airtable with the confirmed time
            update_record(conversations[from_number]['record_id'], {
                'Photography Scheduled': 'Yes',
                'Photography Scheduled Date': confirmed_time,
            })

            # End the scheduling conversation
            conversations[from_number]['scheduling'] = False

            resp = MessagingResponse()
            resp.message(f"Thanks! You're confirmed for {confirmed_time}. Please upload the photos to your portal at domicileai.com. Thanks!")
            return str(resp)
        else:
            # The photographer has not replied with a time, we send a follow up question
            resp = MessagingResponse()
            resp.message(response)
            return str(resp)
    
    if last_question is not None:
        print(f"Last question was: {last_question['question']}")  # Debug: What was the last question asked
        validation_message = None
        if 'validator' in last_question:
            validation_message = last_question['validator'](body)

        if validation_message is not None:
            # the response is not valid, ask the validation error message
            resp = MessagingResponse()
            resp.message(validation_message)
            return str(resp)

        last_question['response'] = body
        conversations[from_number][last_question['field']] = last_question
        print(f"Response to {last_question['field']} was {body}")  # Debug: What was the response to the last question

    next_question = get_next_question(from_number)

    if next_question is not None:
        print(f"Next question is {next_question['question']}")  # Debug: What is the next question
        resp = MessagingResponse()
        resp.message(next_question['question'])
    else:
        conversation = conversations[from_number]
        formatted_conversation = format_conversation(conversation)
        formatted_conversation['Phone Number'] = from_number
        print(f"Formatted Conversation: {formatted_conversation}")
        formatted_conversation["Role"] = formatted_conversation["Role"].strip()
        
         # Fetch the Airtable records
        records = get_records()

        # Find the record that matches the phone number
        record_id = None
        for record in records:
            if 'Phone Number' in record['fields']:
                record_phone_number = record['fields']['Phone Number']
                if record_phone_number == from_number:
                    record_id = record['id']
                    break
            else:
                print("Phone Number not found in the record")

        if record_id is None:
            print(f"Could not find a record with phone number {from_number}")
            resp = MessagingResponse()
            resp.message('Something went wrong. Please try again later.')
            return str(resp)

        # Update the record in Airtable
        if not update_record(record_id,             formatted_conversation):
            resp = MessagingResponse()
            resp.message('Something went wrong. Please try again later.')
            return str(resp)
        resp = MessagingResponse()
        resp.message('Thanks! Your responses have been recorded.')
        print(f"Outgoing message to {from_number}: Thanks! Your responses have been recorded.")  # Print outgoing messages for debugging

    return str(resp)

@app.route('/newrecord', methods=['POST'])
def new_record():
    data = request.get_json()
    to_number = data.get('phone')
    print("To Number: ", to_number)  # Print the 'To' number for debugging
    send_sms(to_number, questions[0]['question'])
    conversations[to_number] = {}
    return 'Record created', 201

#This route is meant to be called when an airtable record is updated with "needing photography". It is meant to find times that work and starts a conversation with a photographer about it to get it scheduled. This route takes as input a post request (designed to be from Zapier) which takes in request data and calls the scheduler engine to find photosgraphy times.
@app.route('/schedulephotography', methods=['POST'])
def schedule_photography():
    record_id = request.form.get('record_id')
    phone_number = request.form.get('Phone Number')
    start_date = request.form.get('Tenant Move Out Date')
    end_date = request.form.get('Desired Lease Start Date')
    address = request.form.get('Property Address')
    # Get recommended photography times
    times = get_photography_times(start_date, end_date)
    # Add to the conversation log
    convos_log = [f"From Domicile AI: New photography task. Best times for photos: {times}. Property address: {address}. Please confirm if one of these works for you or propose a new time!"]

    # Store the conversation log and the scheduling status in the conversations
    if phone_number not in conversations:
        conversations[phone_number] = {}
    conversations[phone_number]['convos_log'] = convos_log
    conversations[phone_number]['scheduling'] = True
    conversations[phone_number]['record_id'] = record_id

    # Start a conversation with the photographer
    send_sms(phone_number, " ".join(convos_log))

    return "Photography scheduling initiated.", 200

if __name__ == "__main__":
    app.run(debug=True)

