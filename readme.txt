

Purpose: Applicaiton which, given a trigger, starts an SMS conversation with a user and stores responses. Fills in fields in airtable record


Needed:
export TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXX
export TWILIO_AUTH_TOKEN=your_auth_token
export AIRTABLE_API_KEY=XXXXXXXXXXX
python app.py


Steps to test locally:
1. set twilio env vars
  export TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXX
  export TWILIO_AUTH_TOKEN=your_auth_token
2. run ngrok - go to ngrok website and expose a port 
  a. enter into terminal
      ngrok http 5000
    To expose server to internet
  b. Enter the forwarding address from NGROK into twilio console under phone number > messaging service
  c. make sure forwarding address
3. to simulate trigger (new recorg)
   curl -X POST -H "Content-Type: application/json" -d '{"phone": "+15417847855"}' http://localhost:5000/newrecord



To do:
1. Finish questions
2. Set up Zapier so it actually works
3. finalize dataset export and pulldown to airtable / salesforce
4. Make a config for quesitons and keys



Directory:
app/
├── main.py # Main application file
├── config.py # Configuration file, contains API keys etc.
├── questions.py # Contains the questions for the survey
├── utils/ # Utilities directory
│ ├── openai_utils.py # Contains utility functions for working with OpenAI
│ ├── airtable_utils.py # Contains utility functions for working with Airtable
│ ├── sms_utils.py # Contains utility functions for sending SMS messages
│ └── validation_utils.py # Contains utility functions for validation

Each file is described below:

- `main.py`: This is the main application file. It contains the Flask application and routes for handling incoming SMS messages.

- `config.py`: This file contains the configuration for the application. It should include your API keys for Twilio, OpenAI, and Airtable.

- `questions.py`: This file contains the questions for your SMS survey. They should be defined as a list of dictionaries.

- `openai_utils.py`: This file contains utility functions for working with the OpenAI API. This includes formatting the conversation for use with the GPT-3 model.

- `airtable_utils.py`: This file contains utility functions for interacting with Airtable. This includes getting records and updating records.

- `sms_utils.py`: This file contains utility functions for sending SMS messages via Twilio.

- `validation_utils.py`: This file contains utility functions for validating user responses to survey questions.



//////////////////////////

SMS Chatbot for Real Estate Listing
This is a simple Python-based SMS chatbot built using Flask and Twilio APIs. It asks users a series of questions about a property they wish to list for rent. Responses are then validated and stored into an Airtable base.

Prerequisites
Python
Flask
Twilio Python Library
Airtable Python Library
An account with Twilio and Airtable
Setup
Clone or download the project to your local machine.

Install the required libraries using pip:

Copy code
pip install flask twilio airtable-python-wrapper
Set up the following environment variables:

TWILIO_ACCOUNT_SID: Your Twilio Account SID
TWILIO_AUTH_TOKEN: Your Twilio Auth Token
AIRTABLE_BASE_ID: Your Airtable Base ID
AIRTABLE_API_KEY: Your Airtable API Key
AIRTABLE_TABLE_NAME: Your Airtable Table Name
You can set environment variables in your shell like this:

arduino
Copy code
export VARIABLE_NAME=VALUE
Alternatively, you can use a Python package like python-dotenv to manage your environment variables.

Run the Application
To run the application locally:

Navigate to the project directory in your terminal.

Start the application by running:

Copy code
python app.py
The application will run on http://localhost:5000.

You'll need to set up a public URL to receive incoming messages from Twilio. You can use a service like ngrok for this.

To start a new record via a POST request, send a JSON object with the phone number to http://localhost:5000/newrecord. For example:

json
Copy code
{
  "phone": "+1234567890"
}
Disclaimer
This is a sample project and should not be used for real estate transactions without proper validation, error handling, and security measures.

Please replace the instructions for setting environment variables and other specific instructions with ones that match your operating system or deployment environment.