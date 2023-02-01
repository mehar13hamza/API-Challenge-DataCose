from datetime import datetime
import json

import requests

BASE_URL = 'https://challenge-automation-engineer-xij5xxbepq-uc.a.run.app'
BEARER_TOKEN = "fFz8Z7OpPTSY7gpAFPrWntoMuo07ACjp"
USERNAME = "datacose"
PASSWORD = "196D1115456D7"



def get_people_data():
    people_url = f'{BASE_URL}/people/'
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
    res = requests.get(people_url, headers=headers, timeout=5)
    data = json.loads(res.text)
    return data


def remove_spaces(string):
    return string.strip()


def reformat_date(date_str):
    date_str = datetime.strptime(date_str, '%d-%m-%Y').date()
    return date_str.strftime('%Y-%m-%d')


def create_contact_data(peoples):
    contact_data = []
    for people in peoples:
        contact_data.append(
            {
                "first_name": remove_spaces(people['fields']['firstName']),
                "last_name": remove_spaces(people['fields']['lastName']),
                "birthdate": reformat_date(people['fields']['dateOfBirth']),
                "email": people['fields']['email'],
                "custom_properties": {
                    "airtable_id": people['id'],
                    "lifetime_value": people['fields']['lifetime_value'].split("$")[1]
                }
            }
        )
    return contact_data


def post_contacts(contact_data):
    contact_url = f"{BASE_URL}/contacts/"
    completion_status = True

    for contact in contact_data:
        response = requests.post(contact_url, auth=(USERNAME, PASSWORD), json=contact, timeout=5)
        if response.status_code != 200:
            completion_status = False

    return completion_status


if __name__ == '__main__':
    people_data = get_people_data()
    contacts = create_contact_data(people_data)
    final_status = post_contacts(contacts)
    if final_status:
        print("Successful")
    else:
        print("Not Successful")
