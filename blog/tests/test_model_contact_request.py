import time

from django.core.exceptions import ValidationError
from django.test import TestCase

from blog.models import ContactRequest


class ContactRequestTestCase(TestCase):
    def setUp(self) -> None:
        self.cr: ContactRequest = ContactRequest.objects.create(name="My Name", email="my@test.com",
                                                                content="test content")

    def test_contact_request_retrieve(self) -> None:
        contact_request = ContactRequest.objects.get(name="My Name")
        self.assertEqual("My Name", contact_request.name)
        self.assertEqual("my@test.com", contact_request.email)

    def test_contact_request_name_required(self) -> None:
        cr1: ContactRequest = ContactRequest(name="  ", email="my@test.com", content="test content")
        cr2: ContactRequest = ContactRequest(email="my@test.com", content="test content")
        with self.assertRaises(ValidationError) as error1:
            cr1.full_clean()
        with self.assertRaises(ValidationError) as error2:
            cr2.full_clean()
        msg1: str = error1.exception.message_dict['name'][0]
        msg2: str = error2.exception.message_dict['name'][0]
        self.assertTrue(all(word in msg1 for word in ['empty', 'blanks']))
        self.assertTrue(all(word in msg2 for word in ['cannot', 'blank']))

    def test_contact_request_name_max_length(self) -> None:
        cr: ContactRequest = ContactRequest(name="My Name" * 100, email="my@test.com", content="test content")
        with self.assertRaises(ValidationError) as error:
            cr.full_clean()
        msg: str = error.exception.message_dict['name'][0]
        self.assertTrue(all(word in msg for word in ['at most', 'characters']))

    def test_contact_request_email_required(self) -> None:
        cr: ContactRequest = ContactRequest(name="My Name", content="test content")
        with self.assertRaises(ValidationError) as error:
            cr.full_clean()
        msg: str = error.exception.message_dict['email'][0]
        self.assertTrue(all(word in msg for word in ['cannot', 'blank']))

    def test_contact_request_content_required(self) -> None:
        cr1: ContactRequest = ContactRequest(name="My Name", email="my@test.com", content="  ")
        cr2: ContactRequest = ContactRequest(name="My Name", email="my@test.com")
        with self.assertRaises(ValidationError) as error1:
            cr1.full_clean()
        with self.assertRaises(ValidationError) as error2:
            cr2.full_clean()
        msg1: str = error1.exception.message_dict['content'][0]
        msg2: str = error2.exception.message_dict['content'][0]
        self.assertTrue(all(word in msg1 for word in ['empty', 'blanks']))
        self.assertTrue(all(word in msg2 for word in ['cannot', 'blank']))

    def test_contact_request_email_validation(self) -> None:
        cr: ContactRequest = ContactRequest(name="My Name", email="mytest.com", content="test content")
        with self.assertRaises(ValidationError) as error:
            cr.full_clean()
        msg: str = error.exception.message_dict['email'][0]
        self.assertTrue(all(word in msg for word in ['valid', 'email']))

    def test_contact_request_pub_dttm_order(self) -> None:
        time.sleep(0.01)  # wait 0.01 second to make sure the pub_dttm is different from self.cr
        cr = ContactRequest.objects.create(name="My Name", email="my@test.com", content="test content")
        self.assertGreater(cr.pub_dttm, self.cr.pub_dttm)
