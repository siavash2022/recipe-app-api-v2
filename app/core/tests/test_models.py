"""
Test for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelsTests(TestCase):
    """ Tests models. """

    def test_create_user_with_email_successful(self):
        """ Test creating user with email is successful. """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password  = password,
        )

        self.assertEqual(user.email , email)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_superuser(
            email = email,
            password  = password,
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)