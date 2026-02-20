from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage


class ContactFormTest(TestCase):
    def test_contact_form_submission(self):
        response = self.client.post(
            reverse("contact:form"),
            {
                "name": "John Doe",
                "email": "john@example.com",
                "subject": "Hello",
                "message": "I want to discuss a project.",
            },
        )
        self.assertRedirects(response, reverse("contact:success"))
        self.assertEqual(ContactMessage.objects.count(), 1)
