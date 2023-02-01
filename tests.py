from unittest import TestCase

from script import remove_spaces, reformat_date, get_people_data, create_contact_data, post_contacts


class ScriptTests(TestCase):
    def test_remove_spaces(self):
        text = remove_spaces("    hello     ")
        self.assertEqual(text, 'hello')

    def test_date_format(self):
        date = reformat_date("13-01-1997")
        self.assertEqual(date, '1997-01-13')

    def test_get_people_date(self):
        data = get_people_data()

        expected_response = {
                        "id": "rec123456789",
                        "fields": {
                            "firstName": " James",
                            "lastName": "Larry",
                            "dateOfBirth": "31-01-1986",
                            "email": "jlarry@example.co",
                            "lifetime_value": "$125500.00"
                        }
                    }

        self.assertEqual(data[0], expected_response)

    def test_create_contact_data(self):
        test_data = [
            {
                "id": "rec132457689",
                "fields": {
                    "firstName": "      John     ",
                    "lastName": "       Doe      ",
                    "dateOfBirth": "31-01-1973",
                    "email": "john@example.co",
                    "lifetime_value": "$229.00"
                }
            }
        ]
        data = create_contact_data(test_data)

        expected_data = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'birthdate': '1973-01-31',
                'email': 'john@example.co',
                'custom_properties':
                    {
                        'airtable_id': 'rec132457689',
                        'lifetime_value': '229.00'
                    }
            }
        ]

        self.assertEqual(data, expected_data)

    def test_post_contacts_successful(self):
        data = expected_data = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'birthdate': '1973-01-31',
                'email': 'john@example.co',
                'custom_properties':
                    {
                        'airtable_id': 'rec132457689',
                        'lifetime_value': '229.00'
                    }
            }
        ]
        status = post_contacts(data)

        self.assertEqual(status, True)

    def test_post_contacts_unsuccessful(self):
        data = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'birthdate': '01-31-1999',
                'email': 'john@example.co',
                'custom_properties':
                    {
                        'airtable_id': 'rec132457689',
                        'lifetime_value': '229.00'
                    }
            }
        ]
        status = post_contacts(data)

        self.assertEqual(status, False)
