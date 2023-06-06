from utils.validation_utils import is_address_valid

questions = [
    {
        'field': 'Role',
        'question': "Hey! I'm Joe's AI. I'm here to help you and Joe get your listing on the market ASAP. It looks like you're a landlord looking to lease your property, is that right?",
        'response': None,
    },
    {
        'field': 'Property Address',
        'question': "Could you send me the full property address?",
        'response': None,
        'validator': is_address_valid
    },
    {
        'field': 'Is Tenant',
        'question': "Does the property currently have a tenant?",
        'response': None
    },
    {
        'field': 'Tenant Move Out Date',
        'question': "When does the current tenant move out?",
        'response': None,
        'conditions': [{'field': 'Is Tenant', 'response': 'yes'}]  # this question will be asked only if 'Is Tenant' was answered with 'yes'
    },
    {
        'field': 'Desired Lease Start Date',
        'question': "What is your desired lease start date?",
        'response': None,
    },
    {
        'field': 'Photography Needed',
        'question': "Do you need photos taken?",
        'response': None,
    },
    {
        'field': 'Preferred Communication',
        'question': "What is your preferred communication method?",
        'response': None,
    },
]