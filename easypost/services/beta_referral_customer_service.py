from typing import (
    Any,
    Optional,
)

from easypost.easypost_object import convert_to_easypost_object
from easypost.requestor import (
    RequestMethod,
    Requestor,
)
from easypost.services.base_service import BaseService


class BetaReferralCustomerService(BaseService):
    def add_payment_method(
        self,
        stripe_customer_id: str,
        payment_method_reference: str,
        priority: str = "primary",
    ) -> dict[str, Any]:
        """Add a Stripe payment method to your EasyPost account.

        This endpoint uses a user's personal Stripe account. The `stripe_customer_id`
        and `payment_method_reference` IDs both come from Stripe. By adding these to
        EasyPost, we will associate your Stripe payment method with either your primary
        or secondary EasyPost payment method.
        """
        params = {
            "payment_method": {
                "stripe_customer_id": stripe_customer_id,
                "payment_method_reference": payment_method_reference,
                "priority": priority,
            }
        }

        response = Requestor(self._client).request(
            method=RequestMethod.POST,
            url="/referral_customers/payment_method",
            params=params,
            beta=True,
        )

        return convert_to_easypost_object(response=response)

    def refund_by_amount(self, refund_amount: int) -> dict[str, Any]:
        """Refund a ReferralCustomer wallet by specifying an amount."""
        params = {"refund_amount": refund_amount}

        response = Requestor(self._client).request(
            method=RequestMethod.POST,
            url="/referral_customers/refunds",
            params=params,
            beta=True,
        )

        return convert_to_easypost_object(response=response)

    def refund_by_payment_log(self, payment_log_id: str) -> dict[str, Any]:
        """Refund a ReferralCustomer wallet by specifying a payment log ID to completely refund."""
        params = {"payment_log_id": payment_log_id}

        response = Requestor(self._client).request(
            method=RequestMethod.POST,
            url="/referral_customers/refunds",
            params=params,
            beta=True,
        )

        return convert_to_easypost_object(response=response)

    def create_credit_card_client_secret(self) -> dict[str, Any]:
        """Creates a client secret to use with Stripe when adding a credit card."""
        response = Requestor(self._client).request(
            method=RequestMethod.POST,
            url="/setup_intents",
            beta=True,
        )

        return convert_to_easypost_object(response=response)

    def create_bank_account_client_secret(self, return_url: Optional[str] = None) -> dict[str, Any]:
        """Creates a client secret to use with Stripe when adding a bank account."""
        params = {"return_url": return_url}

        response = Requestor(self._client).request(
            method=RequestMethod.POST,
            url="/financial_connections_sessions",
            params=params if return_url else None,
            beta=True,
        )

        return convert_to_easypost_object(response=response)
