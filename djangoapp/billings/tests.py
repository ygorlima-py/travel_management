from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from expenses.models import Plan
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock

User = get_user_model()

class TestBillings(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpas123"
        )

        self.plan = Plan.objects.create(
            id=5,
            name="Test Plan",
            stripe_price_monthly_id="price_test_monthly",
            stripe_price_yearly_id="price_test_yearly",
        )
    
    @patch('stripe.checkout.Session.create')
    def testing_chckout_stripe(self, mock_stripe_session):
        mock_session = MagicMock()
        mock_session.url = "https://checkout.stripe.com/fake-session"
        mock_stripe_session.return_value = mock_session
        
        self.url = "/billings/checkout/5/monthly/"

        # Usa POST
        response = self.client.post(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        
        # Verifica se retornou a URL
        self.assertEqual(response.json()["url"], "https://checkout.stripe.com/fake-session")
        
        # Verifica se o Stripe foi chamado corretamente
        mock_stripe_session.assert_called_once()