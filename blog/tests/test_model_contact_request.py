import time

from django.core.exceptions import ValidationError
from django.test import TestCase

from blog.models import ContactRequest


class ContactRequestTest(TestCase):
    def setUp(self) -> None:
        self.contact_request: ContactRequest = ContactRequest.objects.create(name="My Name", email="my@test.com",
                                                                             content="test content")

    def test_contact_request_retrieve(self) -> None:
        contact_request: ContactRequest = ContactRequest.objects.get(name="My Name")
        self.assertEqual("My Name", contact_request.name)
        self.assertEqual("my@test.com", contact_request.email)
        self.assertIsNotNone(contact_request.pub_dttm)
        pub_dttm_formatted: str = contact_request.pub_dttm.strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(f'{contact_request.name} {pub_dttm_formatted}', str(contact_request))

    def test_contact_request_delete(self) -> None:
        self.contact_request.delete()
        self.assertEqual(0, ContactRequest.objects.count())

    def test_contact_request_name_max_length(self) -> None:
        contact_request: ContactRequest = ContactRequest(name="x" * 101)
        with self.assertRaises(ValidationError) as error:
            contact_request.full_clean()
        msg: str = error.exception.message_dict['name'][0]
        self.assertTrue(all(word in msg for word in ['at most', 'characters']))

    def test_contact_request_email_validation(self) -> None:
        contact_request: ContactRequest = ContactRequest(email="mytest.com")
        with self.assertRaises(ValidationError) as error:
            contact_request.full_clean()
        msg: str = error.exception.message_dict['email'][0]
        self.assertTrue(all(word in msg for word in ['valid', 'email']))

    def test_contact_request_pub_dttm_order(self) -> None:
        time.sleep(0.01)  # wait 0.01 second to make sure the pub_dttm is different from self.contact_request
        contact_request: ContactRequest = ContactRequest.objects.create(name="My Name")
        self.assertGreater(contact_request.pub_dttm, self.contact_request.pub_dttm)
