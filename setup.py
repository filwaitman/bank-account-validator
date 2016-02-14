from setuptools import setup

VERSION = '0.1'


setup(
    name='bank-account-validator',
    packages=['bank_account_validator', ],
    version=VERSION,
    author='Filipe Waitman',
    author_email='filwaitman@gmail.com',
    install_requires=[x.strip() for x in open('requirements.txt').readlines()],
    tests_require=[x.strip() for x in open('requirements_test.txt').readlines()],
    url='https://github.com/filwaitman/bank-account-validator',
    download_url='https://github.com/filwaitman/bank-account-validator/tarball/{}'.format(VERSION),
    keywords=[],
    test_suite='tests',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ]
)
