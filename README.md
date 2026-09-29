# afconwave — Official Python SDK

```python
from afconwave import AfconWave

afc = AfconWave(secret_key="afc_sk_test_your_key_here")
```

Sandbox: `afc_sk_test_`. Live: `afc_sk_live_`.

```python
ok = AfconWave.verify_webhook_signature(payload, signature, secret)
event_name = event.get("type") or event.get("event")
```
