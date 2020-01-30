Bank Account Validator
=======================

Python implementation for bank account validation.

Currently, the biggest Brazilian banks are implemented - and so being validated. There is no other countries' banks implemented, but the code is modular and it can be done easily.

Usage:

.. code:: python

    from bank_account_validator.core import Bank
    bank_class = Bank.get('bank_code', 'country_code')
    bank_class(branch='branch', branch_digit='branch_digit',
               account='account', account_digit='account_digit').execute()



Examples:

.. code:: python

    from bank_account_validator.core import Bank, BrazilianBank

    # Account below is correct, so nothing is raised by calling execute()
    bank_class = Bank.get('237', 'BR')
    bank_class(branch='1769', branch_digit='8', account='200040', account_digit='7').execute()

    # Account below has invalid branch so InvalidBranch will be raised
    bank_class = BrazilianBank.get('237')
    bank_class(branch='1769', branch_digit='0', account='200040', account_digit='7').execute()
    # InvalidBranch: Branch "1769-0" is wrong.

    # Account below has invalid account so InvalidAccount will be raised
    bank_class = BrazilianBank.get('237')
    bank_class(branch='1769', branch_digit='8', account='200040', account_digit='0').execute()
    # InvalidAccount: Account "0200040-0" is wrong.

    # Sometimes there is not an unitary validation for both branch and account
    # I mean, the full combination is evaluated at once.
    bank_class = BrazilianBank.get('033')
    bank_class(branch='2006', branch_digit='', account='01008407', account_digit='1').execute()
    # InvalidBranchAndAccountCombination: Combination (branch="2006", account="01008407-1") does not match.

    # It also validates wether digits must be supplied or not, as well as branch/account lengths
    bank_class = BrazilianBank.get('237')
    bank_class(branch='111769', branch_digit='8', account='200040', account_digit='7').execute()
    # InvalidBranchlength: For bank code "237", branches length must be 4.

    bank_class(branch='1769', branch_digit='8', account='11200040', account_digit='7').execute()
    # InvalidAccountlength: For bank code "237", accounts length must be 7.

    bank_class(branch='1769', branch_digit='', account='200040', account_digit='7').execute()
    # MissingBranchDigit: For bank code "237", branches must have a digit, of length 1.

    bank_class(branch='1769', branch_digit='11', account='200040', account_digit='7').execute()
    # UnexpectedBranchDigit: For bank code "237", branches must have 1 digits.

    bank_class(branch='1769', branch_digit='8', account='200040', account_digit='').execute()
    # MissingAccountDigit: For bank code "237", accounts must have a digit, of length 1.

    bank_class(branch='1769', branch_digit='8', account='200040', account_digit='11').execute()
    # UnexpectedAccountDigit: For bank code "237", accounts must have 1 digits.



Contribute
----------

Did you think in some interesting feature, or have you found a bug? Please let me know!

Of course you can also download the project and send me some `pull requests <https://github.com/filwaitman/bank-account-validator/pulls>`_.


You can send your suggestions by `opening issues <https://github.com/filwaitman/bank-account-validator/issues>`_.

You can contact me directly as well. Take a look at my contact information at `http://filwaitman.github.io/ <http://filwaitman.github.io/>`_ (email is preferred rather than mobile phone).
