from typing import (
    Any,
    Dict,
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
    ) -> Dict[str, Any]:
        """Add a Stripe payment method to your EasyPost account.

        This endpoint uses a user's personal Stripe account. The `stripe_customer_id`
        and `payment_method_reference` IDs both come from Stripe. By adding these to
        EasyPost, we will associate your Stripe payment method with either your primary
        or secondary EasyPost payment method.
        """
        wrapped_params = {
            "payment_method": {
                "stripe_customer_id": stripe_customer_id,
                "payment_method_reference": payment_method_reference,
                "priority": priority,
            }
        }

        response = Requestor(self._client).request(
            method=RequestMethod.POST,
            url="/referral_customers/payment_method",
            params=wrapped_params,
            beta=True,
        )

        return convert_to_easypost_object(response=response)

    def refund_by_amount(self, refund_amount: int) -> Dict[str, Any]:
        """Refund a ReferralCustomer wallet by specifying an amount."""
        wrapped_params = {"refund_amount": refund_amount}

        response = Requestor(self._client).request(
            method=RequestMethod.POST,
            url="/referral_customers/refunds",
            params=wrapped_params,
            beta=True,
        )

        return convert_to_easypost_object(response=response)

    def refund_by_payment_log(self, payment_log_id: str) -> Dict[str, Any]:
        """Refund a ReferralCustomer wallet by specifying a payment log ID to completely refund."""
        wrapped_params = {"payment_log_id": payment_log_id}

        response = Requestor(self._client).request(
            method=RequestMethod.POST,
            url="/referral_customers/refunds",
            params=wrapped_params,
            beta=True,
        )

        return convert_to_easypost_object(response=response)
