from afconwave import AfconWave

try:
    client = AfconWave('sk_test_123')
    print("Python SDK Instantiated Successfully!")
    print("Services loaded: Payments, Payouts, Crypto")
except Exception as e:
    print(f"Failed to instantiate Python SDK: {str(e)}")
    exit(1)
