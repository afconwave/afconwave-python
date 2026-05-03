# afconwave — Official Python SDK

> The official Python client library for the AfconWave Payments API.

[![PyPI version](https://img.shields.io/pypi/v/afconwave.svg)](https://pypi.org/project/afconwave/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Features

- ✅ Python 3.8+ compatible
- 🌍 Payments, Payouts, and Refunds in one library
- 🔒 Secure API key handling
- 🔔 Webhook signature verification helper
- 🧪 Sandbox-ready with test keys

---

## Installation

```bash
pip install afconwave
```

---

## Quick Start

```python
from afconwave import AfconWave

afw = AfconWave(secret_key="sk_test_your_key_here")
```

---

## Usage Guide

### Create a Payment

```python
payment = afw.create_payment(
    amount=5000,            # Amount in minor units (5000 = 50 XAF)
    currency="XAF",
    description="Order #1234",
    callback_url="https://yoursite.com/payment/callback",
    customer={
        "name": "Jean Dupont",
        "email": "jean@example.com",
        "phone": "+237600000000",
    },
    metadata={"order_id": "ORD-1234"}
)

print(payment["checkout_url"])  # Redirect user here
print(payment["id"])            # e.g., pay_507f191e8180f
```

### Retrieve a Payment

```python
payment = afw.retrieve_payment("pay_507f191e8180f")

print(payment["status"])   # "pending" | "success" | "failed"
print(payment["amount"])
print(payment["paid_at"])
```

### Create a Payout

```python
payout = afw.create_payout(
    amount=10000,
    currency="XAF",
    recipient={
        "phone": "+237600000001",
        "network": "MTN",  # "MTN" | "ORANGE" | "MOOV" | "WAVE"
        "name": "Marie Kamga",
    },
    reference="PAYOUT-REF-001"
)

print(payout["status"])  # "pending" | "success" | "failed"
```

### List Payments

```python
result = afw.list_payments(limit=20, status="success")

for payment in result["data"]:
    print(payment["id"], payment["amount"], payment["status"])
```

---

## Webhook Verification

Verify that incoming webhooks are genuinely from AfconWave:

```python
import hashlib
import hmac
from flask import Flask, request, abort

app = Flask(__name__)
WEBHOOK_SECRET = "your_webhook_secret"

@app.route("/webhooks/afconwave", methods=["POST"])
def handle_webhook():
    signature = request.headers.get("X-AfconWave-Signature", "")
    payload = request.get_data(as_text=True)

    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        abort(400, "Invalid signature")

    event = request.get_json()

    if event["event"] == "payment.success":
        print("Payment received:", event["data"]["id"])
    elif event["event"] == "payment.failed":
        print("Payment failed")
    elif event["event"] == "payout.success":
        print("Payout delivered")

    return "OK", 200
```

---

## Error Handling

```python
from afconwave import AfconWave, AfconWaveError

afw = AfconWave(secret_key="sk_test_...")

try:
    payment = afw.create_payment(amount=5000, currency="XAF", callback_url="...")
except AfconWaveError as e:
    print(f"API Error {e.status_code}: {e.message}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Configuration

| Parameter | Type | Default | Description |
|---|---|---|---|
| `secret_key` | `str` | **required** | Your AfconWave secret API key |
| `base_url` | `str` | `https://api.afconwave.com/v1` | API base URL |
| `timeout` | `int` | `30` | Request timeout (seconds) |

---

## Sandbox / Testing

Use test keys prefixed with `sk_test_` for sandbox mode. No real transactions occur.

```python
afw = AfconWave(secret_key="sk_test_...")
```

---

## Django / Flask Integration

### Django (example view)

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from afconwave import AfconWave

afw = AfconWave(secret_key="sk_live_...")

def create_checkout(request):
    payment = afw.create_payment(
        amount=int(request.POST["amount"]),
        currency="XAF",
        callback_url="https://yoursite.com/payment/success",
    )
    return JsonResponse({"checkout_url": payment["checkout_url"]})
```

---

## Documentation

Full API documentation: [docs.afconwave.com](https://docs.afconwave.com)

---

## License

MIT © AfconWave
