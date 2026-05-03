from setuptools import setup, find_packages

setup(
    name="afconwave",
    version="0.1.0",
    description="Official AfconWave Python SDK",
    author="AfconWave Team",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
