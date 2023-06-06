# utils/airtable_utils.py
from airtable import Airtable
from config import AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME

def get_airtable():
    return Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, api_key=AIRTABLE_API_KEY)

def get_records():
    airtable = get_airtable()
    return airtable.get_all()

def update_record(record_id, data):
    airtable = get_airtable()
    try:
        airtable.update(record_id, data)
        return True
    except Exception as e:
        print(f"Failed to update record in Airtable: {e}")
        return False
