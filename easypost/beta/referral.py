from typing import (
    Any,
    Dict,
    List,
    Optional,
)

import requests

from easypost.easypost_object import convert_to_easypost_object
from easypost.error import Error
from easypost.requestor import (
    RequestMethod,
    Requestor,
)


class Referral:
    @staticmethod
    def create(
        api_key: Optional[str] = None,
        **params,
    ) -> Dict[str, Any]:
        """Create a referral user.

        This function requires the Partner User's API key.
        """
        requestor = Requestor(local_api_key=api_key)
        new_params = {"user": params}
        response, api_key = requestor.request(
            method=RequestMethod.POST,
            url="/referral_customers",
            params=new_params,
            beta=True,
        )
        return convert_to_easypost_object(response=response, api_key=api_key)

    @staticmethod
    def update_email(
        email,
        user_id,
        api_key: Optional[str] = None,
    ) -> bool:
        """Update a referral user.

        This function requires the Partner User's API key.
        """
        requestor = Requestor(local_api_key=api_key)
        url = f"/referral_customers/{user_id}"
        wrapped_params = {
            "user": {
                "email": email,
            }
        }
        _, _ = requestor.request(
            method=RequestMethod.PUT,
            url=url,
            params=wrapped_params,
            beta=True,
        )

        # Return true if succeeds, an error will be thrown if it fails
        return True

    @staticmethod
    def all(
        api_key: Optional[str] = None,
        **params,
    ) -> List:
        """Retrieve a list of referral users.

        This function requires the Partner User's API key.
        """
        requestor = Requestor(local_api_key=api_key)
        response, api_key = requestor.request(
            method=RequestMethod.GET,
            url="/referral_customers",
            params=params,
            beta=True,
        )
        return convert_to_easypost_object(response=response, api_key=api_key)

    @staticmethod
    def add_credit_card(
        referral_api_key: str,
        number: str,
        expiration_month: int,
        expiration_year: int,
        cvc: str,
        primary_or_secondary: str = "primary",
    ) -> Dict[str, Any]:
        """Add credit card to a referral user.

        This function requires the Referral User's API key.
        """
        easypost_stripe_api_key = Referral._retrieve_easypost_stripe_api_key()

        try:
            stripe_token = Referral._create_stripe_token(
                number, expiration_month, expiration_year, cvc, easypost_stripe_api_key
            )
        except Exception:
            raise Error(message="Could not send card details to Stripe, please try again later")

        response = Referral._create_easypost_credit_card(
            referral_api_key,
            stripe_token.get("id", ""),
            priority=primary_or_secondary,
        )
        return convert_to_easypost_object(response)

    @staticmethod
    def _retrieve_easypost_stripe_api_key() -> str:
        """Retrieve EasyPost's Stripe public API key."""
        requestor = Requestor()
        public_key, _ = requestor.request(
            method=RequestMethod.GET,
            url="/partners/stripe_public_key",
            beta=True,
        )
        return public_key.get("public_key", "")

    @staticmethod
    def _create_stripe_token(
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
        )
        return stripe_response.json()

    @staticmethod
    def _create_easypost_credit_card(
        referral_api_key: str,
        stripe_object_id: str,
        priority: str = "primary",
    ) -> Dict[str, Any]:
        """Submit Stripe credit card token to EasyPost."""
        requestor = Requestor(local_api_key=referral_api_key)

        params = {
            "credit_card": {
                "stripe_object_id": stripe_object_id,
                "priority": priority,
            }
        }

        response, _ = requestor.request(
            method=RequestMethod.POST,
            params=params,
            url="/credit_cards",
            beta=True,
        )
        return response
