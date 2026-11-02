"""Official AfconWave Python SDK for API v2."""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any, Dict, Optional

import requests

__version__ = "2.0.0"


class AfconWaveError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None, code: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(self.message)


class AuthError(AfconWaveError):
    def __init__(self, message: str = "Invalid API Key"):
        super().__init__(message, status_code=401, code="AUTH_ERROR")


class Resource:
    def __init__(self, client: "AfconWave"):
        self.client = client


class Deposits(Resource):
    def create(self, **kwargs: Any) -> Dict[str, Any]:
        return self.client.request("POST", "/deposits", data=kwargs, idempotency_key=kwargs.get("idempotency_key"))

    def retrieve(self, reference: str) -> Dict[str, Any]:
        return self.client.request("GET", f"/deposits/{reference}")

    def list(self, **kwargs: Any) -> Dict[str, Any]:
        return self.client.request("GET", "/deposits", params=kwargs)

    def sync(self, reference: str) -> Dict[str, Any]:
        return self.client.request("POST", f"/deposits/{reference}/sync")


class Withdrawals(Resource):
    def create(self, **kwargs: Any) -> Dict[str, Any]:
        return self.client.request("POST", "/withdrawals", data=kwargs, idempotency_key=kwargs.get("idempotency_key"))

    def list(self, **kwargs: Any) -> Dict[str, Any]:
        return self.client.request("GET", "/withdrawals", params=kwargs)

    def sync(self, reference: str) -> Dict[str, Any]:
        return self.client.request("POST", f"/withdrawals/{reference}/sync")

    def methods(self, country_code: str) -> Dict[str, Any]:
        return self.client.request("GET", "/withdrawals/methods", params={"country_code": country_code})

    def nigeria_banks(self) -> Dict[str, Any]:
        return self.client.request("GET", "/withdrawals/nigeria-banks")


class Wallets(Resource):
    def list(self, **kwargs: Any) -> Dict[str, Any]:
        return self.client.request("GET", "/wallets", params=kwargs)

    def ensure(self, currency: str, business_id: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"currency": currency}
        if business_id:
            body["business_id"] = business_id
        return self.client.request("POST", "/wallets/ensure", data=body)

    def convert(self, **kwargs: Any) -> Dict[str, Any]:
        return self.client.request("POST", "/wallets/convert", data=kwargs, idempotency_key=kwargs.get("idempotency_key"))

    def transfer(self, **kwargs: Any) -> Dict[str, Any]:
        return self.client.request("POST", "/wallets/transfer", data=kwargs, idempotency_key=kwargs.get("idempotency_key"))

    def rates(self) -> Dict[str, Any]:
        return self.client.request("GET", "/wallets/rates")


class Transactions(Resource):
    def list(self, **kwargs: Any) -> Dict[str, Any]:
        return self.client.request("GET", "/transactions", params=kwargs)

    def retrieve(self, id_or_ref: str) -> Dict[str, Any]:
        return self.client.request("GET", f"/transactions/{id_or_ref}")

    def recent(self, limit: int = 4) -> Dict[str, Any]:
        return self.client.request("GET", "/transactions/recent", params={"limit": limit})


class Refunds(Resource):
    def create(self, **kwargs: Any) -> Dict[str, Any]:
        return self.client.request("POST", "/refunds", data=kwargs)

    def list(self) -> Dict[str, Any]:
        return self.client.request("GET", "/refunds")


class Disputes(Resource):
    def open(self, **kwargs: Any) -> Dict[str, Any]:
        return self.client.request("POST", "/disputes", data=kwargs)

    def list(self) -> Dict[str, Any]:
        return self.client.request("GET", "/disputes")


class Airtime(Resource):
    def purchase(self, **kwargs: Any) -> Dict[str, Any]:
        return self.client.request("POST", "/airtime", data=kwargs)


class DataPlans(Resource):
    def purchase(self, **kwargs: Any) -> Dict[str, Any]:
        return self.client.request("POST", "/data", data=kwargs)


class PaymentLinks(Resource):
    def create(self, **kwargs: Any) -> Dict[str, Any]:
        return self.client.request("POST", "/payment-links", data=kwargs)

    def list(self) -> Dict[str, Any]:
        return self.client.request("GET", "/payment-links")


class Rails(Resource):
    def payout_methods(self, country_code: str) -> Dict[str, Any]:
        return self.client.request("GET", "/rails/payout-methods", params={"country_code": country_code})


class AfconWave:
    """
    AfconWave API v2 client.

    Auth: X-API-Key with afcw_test_... or afcw_live_...
    Base: https://api.afconwave.com/v1
    """

    def __init__(
        self,
        secret_key: str,
        base_url: Optional[str] = None,
        timeout: int = 30,
        sandbox: bool = False,
    ):
        if not secret_key or not secret_key.startswith("afcw_"):
            raise AuthError("secret_key must be an afcw_test_... or afcw_live_... key")

        self.secret_key = secret_key
        self.timeout = timeout

        if base_url:
            self.base_url = base_url.rstrip("/")
        else:
            import os

            env_url = os.environ.get("AFCONWAVE_BASE_URL")
            if env_url:
                self.base_url = env_url.rstrip("/")
            elif sandbox:
                self.base_url = "https://sandbox.api.afconwave.com/v1"
            else:
                self.base_url = "https://api.afconwave.com/v1"

        self.deposits = Deposits(self)
        self.withdrawals = Withdrawals(self)
        self.wallets = Wallets(self)
        self.transactions = Transactions(self)
        self.refunds = Refunds(self)
        self.disputes = Disputes(self)
        self.airtime = Airtime(self)
        self.data = DataPlans(self)
        self.payment_links = PaymentLinks(self)
        self.rails = Rails(self)

        # Back-compat aliases
        self.payments = self.deposits
        self.payouts = self.withdrawals

    @staticmethod
    def verify_webhook_signature(
        payload: str,
        signature: str,
        secret: str,
        tolerance: int = 300,
        timestamp_prefixed: bool = False,
        timestamp: Optional[str] = None,
    ) -> bool:
        if not signature or not secret:
            return False

        message = f"{timestamp}.{payload}" if timestamp_prefixed and timestamp else payload
        expected = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signature):
            return False

        if timestamp:
            try:
                ts = float(timestamp)
                webhook_time = ts / 1000.0 if ts > 1e12 else ts
                if abs(time.time() - webhook_time) > tolerance:
                    return False
            except (ValueError, TypeError):
                pass

        return True

    def request(
        self,
        method: str,
        path: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        headers = {
            "X-API-Key": self.secret_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"AfconWave-Python-SDK/{__version__}",
        }
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        url = f"{self.base_url}{path}"
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                json=data,
                params=params,
                timeout=self.timeout,
            )
            try:
                res_data = response.json()
            except ValueError:
                res_data = {"error": response.text or response.reason}

            if not response.ok:
                msg = res_data.get("error") or response.reason
                if response.status_code == 401:
                    raise AuthError(msg)
                raise AfconWaveError(message=msg, status_code=response.status_code, code=res_data.get("code"))

            return res_data
        except requests.exceptions.RequestException as e:
            raise AfconWaveError(message=str(e))

    def get_balances(self, **kwargs: Any) -> Any:
        res = self.wallets.list(**kwargs)
        return res.get("wallets", res)

    def create_payment(self, **kwargs: Any) -> Dict[str, Any]:
        """Deprecated alias for deposits.create."""
        return self.deposits.create(**kwargs)

    def create_payout(self, **kwargs: Any) -> Dict[str, Any]:
        """Deprecated alias for withdrawals.create."""
        return self.withdrawals.create(**kwargs)
