import requests
import hmac
import hashlib

# ─── Exceptions ────────────────────────────────────────────────────────────────

class AfconWaveError(Exception):
    def __init__(self, message, status_code=None, code=None):
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(self.message)

# ─── Resources ────────────────────────────────────────────────────────────────

class Resource:
    def __init__(self, client):
        self.client = client

class Payments(Resource):
    def create(self, **kwargs):
        return self.client.request('POST', '/payments', data=kwargs)
        
    def retrieve(self, payment_id):
        return self.client.request('GET', f'/payments/{payment_id}')
    
    def list(self, **kwargs):
        return self.client.request('GET', '/payments', params=kwargs)

class Payouts(Resource):
    def create(self, **kwargs):
        return self.client.request('POST', '/payouts', data=kwargs)
        
    def retrieve(self, payout_id):
        return self.client.request('GET', f'/payouts/{payout_id}')

class Crypto(Resource):
    def buy(self, **kwargs):
        return self.client.request('POST', '/crypto/buy', data=kwargs)

class Refunds(Resource):
    def create(self, payment_id: str, amount: float, reason: str = None):
        return self.client.request('POST', '/refunds', data={
            'paymentId': payment_id,
            'amount': amount,
            'reason': reason
        })

    def list(self):
        return self.client.request('GET', '/refunds')

class Disputes(Resource):
    def open(self, transaction_id: str, reason: str, description: str):
        return self.client.request('POST', '/disputes', data={
            'transactionId': transaction_id,
            'reason': reason,
            'description': description
        })

    def list(self):
        return self.client.request('GET', '/disputes')

    def resolve(self, dispute_id: str, resolution: str, resolution_details: str = None):
        return self.client.request('POST', f'/disputes/{dispute_id}/resolve', data={
            'resolution': resolution,
            'resolutionDetails': resolution_details
        })

# ─── Main Client ───────────────────────────────────────────────────────────────

class AfconWave:
    def __init__(self, secret_key: str, base_url: str = 'https://api.afconwave.com/v1', timeout: int = 30):
        self.secret_key = secret_key
        self.base_url = base_url
        self.timeout = timeout
        
        self.payments = Payments(self)
        self.payouts = Payouts(self)
        self.crypto = Crypto(self)
        self.refunds = Refunds(self)
        self.disputes = Disputes(self)

    @staticmethod
    def verify_webhook_signature(payload: str, signature: str, secret: str) -> bool:
        """Verifies that an incoming webhook was sent by AfconWave."""
        expected = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    def request(self, method: str, path: str, data: dict = None, params: dict = None):
        headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        url = f"{self.base_url}{path}"
        
        try:
            response = requests.request(
                method, url, headers=headers, json=data, params=params, timeout=self.timeout
            )
            
            res_data = response.json()
            
            if not response.ok:
                raise AfconWaveError(
                    message=res_data.get('error', response.reason),
                    status_code=response.status_code,
                    code=res_data.get('code')
                )
                
            return res_data.get('data', res_data)
            
        except requests.exceptions.RequestException as e:
            raise AfconWaveError(message=str(e))

    # ─── Top-level Convenience Methods (Matches README) ─────────────────────

    def create_payment(self, **kwargs):
        return self.payments.create(**kwargs)

    def retrieve_payment(self, payment_id: str):
        return self.payments.retrieve(payment_id)

    def list_payments(self, **kwargs):
        return self.payments.list(**kwargs)

    def create_payout(self, **kwargs):
        return self.payouts.create(**kwargs)
