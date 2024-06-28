from setuptools import setup, find_packages

setup(
    name='AWS_OCR',
    version='0.1',
    packages=find_packages(),
    install_requires = [
        'boto3',
    ],
)