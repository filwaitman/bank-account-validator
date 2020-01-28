from setuptools import setup

VERSION = '1.0.0'


setup(
    name='bank-account-validator',
    packages=['bank_account_validator',],
    version=VERSION,
    author='Noverde',
    author_email='dev@noverde.com.br',
    install_requires=[x.strip() for x in open('requirements.txt').readlines()],
    tests_require=[
        x.strip() for x in open('requirements_test.txt').readlines()
    ],
    url='https://github.com/noverde/bank-account-validator',
    download_url='https://github.com/noverde/bank-account-validator/tarball/{}'.format(
        VERSION
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
