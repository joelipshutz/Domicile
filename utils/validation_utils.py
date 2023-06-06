

def is_address_valid(address):
    # a very simple address validation - checks if there are at least 5 words in the input
    if len(address.split()) >= 5:
        return None
    else:
        return "That doesn't seem like a full address. Please provide the full property address."