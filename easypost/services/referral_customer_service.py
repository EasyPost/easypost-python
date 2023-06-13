from copy import deepcopy
from typing import (
    Any,
    Dict,
    Optional,
)

import requests
from easypost.constant import (
    SEND_STRIPE_DETAILS_ERROR,
    TIMEOUT,
)
from easypost.easypost_object import convert_to_easypost_object
from easypost.errors import ExternalApiError
from easypost.models import User
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class ReferralCustomerService(BaseService):
    def __init__(self, client):
        self._client = client
        self._model_class = User.__name__

    def create(self, **params) -> User:
        """Create a referral customer.

        This function requires the Partner User's API key.
        """
        wrapped_params = {"user": params}

        response = Requestor(self._client).request(
            method=RequestMethod.POST,
            url="/referral_customers",
            params=wrapped_params,
        )

        return convert_to_easypost_object(response=response)

    def update_email(self, id: str, email: str) -> None:
        """Update a referral customer.

        This function requires the Partner User's API key.
        """
        url = f"/referral_customers/{id}"
        wrapped_params = {
            "user": {
                "email": email,
            }
        }

        Requestor(self._client).request(
            method=RequestMethod.PUT,
            url=url,
            params=wrapped_params,
        )

    def all(self, **params) -> Dict[str, Any]:
        """Retrieve a list of referral customers.

        This function requires the Partner User's API key.
        """
        response = Requestor(self._client).request(
            method=RequestMethod.GET,
            url="/referral_customers",
            params=params,
        )

        return convert_to_easypost_object(response=response)

    def get_next_page(
        self,
        referral_customers: Dict[str, Any],
        page_size: int,
        optional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Retrieve next page of referral customers."""
        return self._get_next_page_resources("referral_customers", referral_customers, page_size, optional_params)

    def add_credit_card(
        self,
        referral_api_key: str,
        number: str,
        expiration_month: int,
        expiration_year: int,
        cvc: str,
        priority: str = "primary",
    ) -> Dict[str, Any]:
        """Add credit card to a referral customer.

        This function requires the ReferralCustomer User's API key.
        """
        easypost_stripe_api_key = self._retrieve_easypost_stripe_api_key()

        try:
            stripe_token = self._create_stripe_token(
                number,
                expiration_month,
                expiration_year,
                cvc,
                easypost_stripe_api_key,
            )
        except Exception:
            raise ExternalApiError(message=SEND_STRIPE_DETAILS_ERROR)

        response = self._create_easypost_credit_card(
            referral_api_key,
            stripe_token.get("id", ""),
            priority=priority,
        )

        return convert_to_easypost_object(response)

    def _retrieve_easypost_stripe_api_key(self) -> str:
        """Retrieve EasyPost's Stripe public API key."""
        public_key = Requestor(self._client).request(
            method=RequestMethod.GET,
            url="/partners/stripe_public_key",
        )

        return public_key.get("public_key", "")

    def _create_stripe_token(
        self,
        number: str,
        expiration_month: int,
        expiration_year: int,
        cvc: str,
        easypost_stripe_key: str,
    ) -> Dict[str, Any]:
        """Get credit card token from Stripe."""
        headers = {
            # This Stripe endpoint only accepts URL form encoded bodies
            "Content-type": "application/x-www-form-urlencoded",
        }

        credit_card_dict = {
            "card": {
                "number": number,
                "exp_month": expiration_month,
                "exp_year": expiration_year,
                "cvc": cvc,
            }
        }

        form_encoded_params = Requestor.form_encode_params(credit_card_dict)
        url = "https://api.stripe.com/v1/tokens"

        stripe_response = requests.post(
            url,
            params=form_encoded_params,
            headers=headers,
            auth=requests.auth.HTTPBasicAuth(easypost_stripe_key, ""),
            timeout=TIMEOUT,
        )

        return stripe_response.json()

    def _create_easypost_credit_card(
        self,
        referral_api_key: str,
        stripe_object_id: str,
        priority: str = "primary",
    ) -> Dict[str, Any]:
        """Submit Stripe credit card token to EasyPost."""
        params = {
            "credit_card": {
                "stripe_object_id": stripe_object_id,
                "priority": priority,
            }
        }

        # Override the API key to use the referral's for this single request
        referral_client = deepcopy(self._client)
        referral_client.api_key = referral_api_key

        response = Requestor(referral_client).request(
            method=RequestMethod.POST,
            params=params,
            url="/credit_cards",
        )

        return response
