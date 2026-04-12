from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User
from django.core import mail

class UserOTPVerificationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/account/register/'
        self.verify_url = '/account/verify-otp/'
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'role': 'job_seeker'
        }

    def test_user_registration_creates_otp_and_sends_email(self):
        # Ensure mail outbox is empty
        self.assertEqual(len(mail.outbox), 0)

        # Register a new user
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify user is created but email is not verified
        user = User.objects.get(email=self.user_data['email'])
        self.assertFalse(user.is_email_verified)
        self.assertIsNotNone(user.otp)
        self.assertIsNotNone(user.otp_expiry)

        # Verify email is sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(user.otp, mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].to, [user.email])

    def test_otp_verification_endpoint(self):
        # First register
        self.client.post(self.register_url, self.user_data, format='json')
        user = User.objects.get(email=self.user_data['email'])

        # Try with invalid OTP
        invalid_data = {
            'email': user.email,
            'otp': '000000'
        }
        res_invalid = self.client.post(self.verify_url, invalid_data, format='json')
        self.assertEqual(res_invalid.status_code, status.HTTP_400_BAD_REQUEST)

        # Try with valid OTP
        valid_data = {
            'email': user.email,
            'otp': user.otp
        }
        res_valid = self.client.post(self.verify_url, valid_data, format='json')
        self.assertEqual(res_valid.status_code, status.HTTP_200_OK)

        # Verify DB changes
        user.refresh_from_db()
        self.assertTrue(user.is_email_verified)
        self.assertIsNone(user.otp)
        self.assertIsNone(user.otp_expiry)
