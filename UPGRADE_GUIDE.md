# Upgrade Guide

Use the following guide to assist in the upgrade process of the `easypost-python` library between major versions.

- [Upgrading from 7.x to 8.0](#upgrading-from-7x-to-80)
- [Upgrading from 6.x to 7.0](#upgrading-from-6x-to-70)
- [Upgrading from 5.x to 6.0](#upgrading-from-5x-to-60)

## Upgrading from 7.x to 8.0

### 8.0 High Impact Changes

- [Updated Dependencies](#80-updated-dependencies)
- [EasyPostClient](#80-easypostclient)
- [Improved Error Handling](#80-improved-error-handling)

### 8.0 Medium Impact Changes

- [Corrected Naming Conventions](#80-corrected-naming-conventions)

### 8.0 Low Impact Changes

- [Beta Namespace Changed](#80-beta-namespace-changed)
- [Changed Function Parameter Order and Return Types](#80-changed-function-parameter-order-and-return-types)

## 8.0 Updated Dependencies

Likelihood of Impact: High

**Python 3.7 Required**

easypost-python now requires Python 3.7 or greater.

**Dependencies**

All dependencies had minor version bumps.

## 8.0 EasyPostClient

Likelihood of Impact: High

This library is now thread-safe with the introduction of a new `EasyPostClient` object. Instead of defining a global API key that all requests use, you create an `EasyPostClient` object and pass your API key to it. You then call your desired functions against a "service" which coincide with EasyPost objects:

```python
# Old method
easypost.api_key = os.getenv('EASYPOST_API_KEY')
shipment = easypost.Shipment.create({'data': 'here'})

# New method
client = easypost.EasyPostClient(api_key=os.getenv('EASYPOST_API_KEY'))
shipment = client.shipment.create({'data': 'here'})
```

All instance methods are now static with the exception of `lowest_rate` as these make API calls and require the EasyPostClient (EasyPost objects do not contain an API key to make API calls with).

Previously used `.save()` instance methods are now static `.update()` functions where you specify first the ID of the object you are updating and second, the parameters that need updating.

Functions no longer accept an API key as an optional parameter. If you need per-function API key changes, create a new EasyPostClient object and call the function on the new client that uses the API key you need.

### 8.0 Improved Error Handling

Likelihood of Impact: High

There are ~2 dozen new error types that extend either `ApiError` or `EasyPostError`.

New ApiErrors (extends EasyPostError):

- `ApiError`
- `EncodingError`
- `ExternalApiError`
- `ForbiddenError`
- `GatewayTimeoutError`
- `HttpError`
- `InternalServerError`
- `InvalidRequestError`
- `JsonError`
- `MethodNotAllowedError`
- `NotFoundError`
- `PaymentError`
- `RateLimitError`
- `RedirectError`
- `ServiceUnavailableError`
- `TimeoutError`
- `UnauthorizedError`
- `UnknownApiError`

New EasyPostErrors (extends builtin Exception):

- `EasyPostError`
- `EndOfPaginationError`
- `FilteringError`
- `InvalidObjectError`
- `InvalidParameterError`
- `MissingParameterError`
- `SignatureVerificationError`

ApiErrors will behave like the previous Error class did. They will include a `message`, `http_status`, and `http_body`. Additionally, a new `code` and `errors` keys are present and populate when available. This class extends the more generic `EasyPostError` which only contains a message, used for errors thrown directly from this library.

The `original_exception` property has been removed and is now returned directly in the error message if present.

### 8.0 Corrected Naming Conventions

Likelihood of Impact: Medium

Occurances of `referral` are now `referral_customer` and `Referral` are now `ReferralCustomer` to match the documentation and API.

Occurances of `smartrate` are now `smart_rate` and `Smartrate` are now `SmartRate` to match the documentation and API.

Occurances of `scanform` are now `scan_form` and `Scanform` are now `ScanForm` to match the documentation and API.

The `primary_or_secondary` parameter name for billing functions is now called `priority` to match the documentation and API.

## 8.0 Beta Namespace Changed

Likelihood of Impact: Low

Previously, the beta namespace was found at `easypost.beta.x` where `x` is the name of your model. Now, the beta namespace is simply prepended to the name of your service: `client.beta_x`. for instance, you can call `client.beta_referral_customer.add_payment_method()`.

## 8.0 Changed Function Parameter Order and Return Types

Likelihood of Impact: Low

The `update_email` function of the `referral_customer` service had the parameter order switched and name changed. Previously, you would pass the email and then the id, Now, you pass the `id` of the user first, then the email. This change matches the rest of the library where an ID always comes first.

Functions that previously returned `True` now do not return anything as there is no response body from the API (eg: `fund_wallet`, `delete_payment_method`, `update_email`, `create_list`)

## Upgrading from 6.x to 7.0

**NOTICE:** v7 is deprecated.

### 7.0 High Impact Changes

- [Updating Dependencies](#70-updating-dependencies)
- [`shipment.lowest_rate()` Now Expects a List](#70-shipmentlowestrate-now-expects-a-list)

### 7.0 Medium Impact Changes

- [Removal of `get_rates()` Shipment Method](#70-removal-of-getrates-shipment-method)

## 7.0 Updating Dependencies

Likelihood of Impact: High

**Python 3.6 Required**

easypost-python now requires Python 3.6 or greater and has dropped support for Python 2.

**Dependencies**

All dependencies had minor version bumps.

## 7.0 `shipment.lowest_rate()` Now Expects a List

Previously the `shipment.lowest_rate()` function expected a comma separated string list of filter criteria (carriers and services). These params have been corrected to expect an actual list object.

```python
# Previous expectation
shipment.lowest_rate(carriers="USPS,FedEx", services="...")

# Current expectation
shipment.lowest_rate(carriers=["USPS", "FedEx"], services=["..."])
```

## 7.0 Removal of `get_rates()` Shipment Method

Likelihood of Impact: Medium

The HTTP method used for the `get_rates` endpoint at the API level has changed from `POST` to `GET` and will only retrieve rates for a shipment instead of regenerating them. A new `/rerate` endpoint has been introduced to replace this functionality; In this library, you can now call the `shipment.regenerate_rates()` method to regenerate rates. Due to the logic change, the `get_rates` method has been removed since a Shipment inherently already has rates associated.

## Upgrading from 5.x to 6.0

**NOTICE:** v6 is deprecated.

### 6.0 High Impact Changes

- [Updating Dependencies](#60-updating-dependencies)
- [JSON Encoded Bodies](#60-json-encoded-bodies)

## 6.0 Updating Dependencies

Likelihood of Impact: High

**Dependencies**

Bumps the `requests` library from v1 to v2.

## 6.0 JSON Encoded Bodies

Likelihood of Impact: High

All `POST` and `PUT` request bodies are now JSON encoded instead of form-encoded. You may see subtle inconsistencies to how certain data types were previously sent to the API. We have taken steps to mitigate and test against these edge cases.
