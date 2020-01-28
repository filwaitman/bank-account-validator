from setuptools import setup

VERSION = '0.1.1'


setup(
    name='bank-account-validator',
    packages=['bank_account_validator'],
    version=VERSION,
    author='Filipe Waitman',
    author_email='filwaitman@gmail.com',
    tests_require=['setuptools==19.1.1', 'nose==1.3.7'],
    url='https://github.com/noverde/bank-account-validator',
    download_url=(
        f'https://github.com/noverde/bank-account-validator/tarball/{VERSION}'
    ),
    keywords=[],
    test_suite='tests',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
)
