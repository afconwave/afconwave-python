# afconwave (Python)

Official **Python SDK** for [AfconWave API v2](https://github.com/afconwave/afconwave-api).

Keys: `afcw_test_…` (sandbox) · `afcw_live_…` (production)  
Auth: `X-API-Key`  
Refs: `AFCW-IN-…` / `AFCW-OUT-…` / `P2P-…` / `FX-…`

```bash
pip install afconwave
```

## Quick start

```python
from afconwave import AfconWave

afc = AfconWave(secret_key="afcw_test_your_key_here")

# Collection
deposit = afc.deposits.create(
    amount=5000,
    country_code="CM",
    currency="XAF",
    payment_method="MTN",
    mobile="670000000",
    mode="direct",
    idempotency_key="order-123",
)

# Payout
payout = afc.withdrawals.create(
    amount=2000,
    currency="XAF",
    country_code="CM",
    payment_method="MTN",
    beneficiary_name="Jane Doe",
    mobile_no="670000001",
)

# Wallets
wallets = afc.wallets.list()
```

## Resources

| Resource | Methods |
|----------|---------|
| `deposits` | `create`, `retrieve`, `list`, `sync` |
| `withdrawals` | `create`, `list`, `sync`, `methods`, `nigeria_banks` |
| `wallets` | `list`, `ensure`, `convert`, `transfer`, `rates` |
| `transactions` | `list`, `retrieve`, `recent` |
| `refunds` / `disputes` | `create`/`open`, `list` |
| `airtime` / `data` | `purchase` |
| `payment_links` | `create`, `list` |
| `rails` | `payout_methods` |

Deprecated aliases: `create_payment` → `deposits.create`, `create_payout` → `withdrawals.create`.

## Breaking changes (v2)

- Auth is **`X-API-Key`**, not Bearer.
- Base path `/v1` (not `/api/v1`).
- `payments` → **`deposits`**; `payouts` → **`withdrawals`**.

## License

MIT
