from afconwave import AfconWave

try:
    client = AfconWave('afcw_sk_test_123')
    print("Python SDK Instantiated Successfully!")
except Exception as e:
    print(f"Failed to instantiate Python SDK: {str(e)}")
    exit(1)
