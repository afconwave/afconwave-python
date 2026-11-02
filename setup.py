from setuptools import setup, find_packages

setup(
    name="afconwave",
    version="2.0.0",
    description="Official AfconWave Python SDK for API v2 — deposits, withdrawals, wallets, FX",
    long_description=open("README.md", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="AfconWave Team",
    author_email="dev@afconwave.com",
    url="https://github.com/afconwave/afconwave-python",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial",
    ],
)
