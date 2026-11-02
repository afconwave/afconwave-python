from afconwave import AfconWave

try:
    client = AfconWave(secret_key="afcw_test_smoke_only")
    print("Python SDK Instantiated Successfully!")
    print("Resources:", [n for n in dir(client) if not n.startswith("_") and not callable(getattr(client, n, None))])
except Exception as e:
    print("Failed:", e)
    raise SystemExit(1)
