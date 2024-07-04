

from setuptools import setup, find_packages

setup(
    name='OCRPackage',
    version='0.1',
    packages=find_packages(),
    install_requires = [
        'google-cloud-vision',
    ],
)