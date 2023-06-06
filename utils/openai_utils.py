import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
def format_conversation(conversation):
    prompt = "You are helping format data to input into airtable. Please only respond with the answer you think is best. Your answer will be used as an input into a database. This was a conversation between us (a real estate company) and a potential client. By the way, the year is 2023 so if they send us a date let's assume that year unless they say otherwise. Here is the conversation:\n"
    for key in conversation:
        question = conversation[key]['question']
        response = conversation[key]['response']
        prompt += f"Q: {question}\nA: {response}\n"
    
    prompt += "\nNow, let's format these answers. Please provide each answer on a new line:\n"
    for key in conversation:
        response = conversation[key]['response']
        if key == 'Role':
            prompt += f"The person said \"{response}\" when asked \"{question}\", what role is this between Landlord, Tenant, Buyer, or Seller\n"
        elif key == 'Property Address':
            prompt += f"When asked for an address, they responded \"{response}\", what's the formatted full address?\n"
        elif key == 'Is Tenant':
            prompt += f"The answer they gave to if there is a tenant is \"{response}\", is this a yes or a no?\n"
        elif key in ['Tenant Move Out Date', 'Desired Lease Start Date']:
            prompt += f"The date provided is \"{response}\", what's the formatted full date in the form of YYYY-MM-DD?\n"
        elif key == 'Photography Needed':
            prompt += f"When asked if photgraphy was needed, they said \"{response}\", Is this a yes or no?\n"
        elif key == 'Preferred Communication':
            prompt += f"The preference for communication given is \"{response}\", is this text or email?\n"
    
    # Call the OpenAI API
    result = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=150)
    print(f"\nPrompt:\n{prompt}")    
    print(f"\nResponse from openAI: \n{result}")
    
    # Split the response into lines
    lines = result.choices[0].text.strip().split('\n')
    
    # Remove any unwanted text before the answers (in this case, the word 'Answer: ')
    lines = [line.replace('Answer: ', '') for line in lines]
    
    # Zip the keys with the lines (formatted responses), and make a new dictionary
    formatted_conversation = dict(zip(conversation.keys(), lines))
    return formatted_conversation

import openai
from datetime import datetime

def get_photography_times(start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    conversation_input = f"we are scheduling a a photography task between {start_date} and {end_date}. Let's try to do these during business hours. Send 3 options for when this could be scheduled."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=conversation_input,
        temperature=0.5,
        max_tokens=100
    )

    # Parsing the response is highly dependent on how your model responds
    # You need to extract the list of recommended times from the response
    # For simplicity, let's assume the response is a comma separated list of times
    recommended_times = response.choices[0].text.strip().split('\n')
    recommended_times = [time.strip() for time in recommended_times]
    
    return recommended_times

import openai

def check_photographer_response(body, conversation):
    # Call to OpenAI
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"""
    {conversation_history}
    Photographer: {latest_response}

    You are an AI model trained to understand and extract information from text. In the above conversation, your task is to identify whether the photographer has confirmed a date and time for the photoshoot. If they have, please extract the date and time in the format YYYY-MM-DD HH:MM:SS. If they have not confirmed, please write a follow-up question to help schedule the photoshoot. It will be sent as is.
    """,  # Define a prompt here
        temperature=0.1,
        max_tokens=200
    )

    # Check the response from OpenAI. If the response contains a valid date and time, return it.
    try:
        valid_datetime = datetime.datetime.strptime(response.choices[0].text.strip(), '%Y-%m-%d %H:%M:%S')
        return valid_datetime.strftime('%Y-%m-%d %H:%M:%S'), True
    except ValueError:
        # If there is no valid date and time in the response, return the response for further follow up.
        return response.choices[0].text.strip(), False
