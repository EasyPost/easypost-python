# Upgrade Guide

Use the following guide to assist in the upgrade process of the `easypost-python` library between major versions.

- [Upgrading from 6.x to 7.0](#upgrading-from-6x-to-70)
- [Upgrading from 5.x to 6.0](#upgrading-from-5x-to-60)

## Upgrading from 6.x to 7.0

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
