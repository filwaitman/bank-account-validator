# -*- coding: utf-8 -*-
class BaseBankAccountValidationError(Exception):
    pass


class BankNotImplemented(BaseBankAccountValidationError):
    def __init__(self, bank_code, country):
        message = (
            'Bank code "{}" is not implemented for country '
            '"{}"- or it does not exist at all.'
        ).format(bank_code, country)
        super(BankNotImplemented, self).__init__(message)


class MissingBranchDigit(BaseBankAccountValidationError):
    def __init__(self, bank):
        message = (
            'For bank code "{}", branches must have a digit, of length {}.'
        ).format(bank.bank_code, bank.branch_digit_length)
        super(MissingBranchDigit, self).__init__(message)


class MissingAccountDigit(BaseBankAccountValidationError):
    def __init__(self, bank):
        message = (
            'For bank code "{}", accounts must have a digit, of length {}.'
        ).format(bank.bank_code, bank.account_digit_length)
        super(MissingAccountDigit, self).__init__(message)


class UnexpectedBranchDigit(BaseBankAccountValidationError):
    def __init__(self, bank):
        message = 'For bank code "{}", branches must have {} digits.'.format(
            bank.bank_code, bank.branch_digit_length
        )
        super(UnexpectedBranchDigit, self).__init__(message)


class UnexpectedAccountDigit(BaseBankAccountValidationError):
    def __init__(self, bank):
        message = 'For bank code "{}", accounts must have {} digits.'.format(
            bank.bank_code, bank.account_digit_length
        )
        super(UnexpectedAccountDigit, self).__init__(message)


class InvalidBranchlength(BaseBankAccountValidationError):
    def __init__(self, bank):
        message = 'For bank code "{}", branches length must be {}.'.format(
            bank.bank_code, bank.branch_length
        )
        super(InvalidBranchlength, self).__init__(message)


class InvalidAccountlength(BaseBankAccountValidationError):
    def __init__(self, bank):
        message = 'For bank code "{}", accounts length must be {}.'.format(
            bank.bank_code, bank.account_length
        )
        super(InvalidAccountlength, self).__init__(message)


class InvalidBranch(BaseBankAccountValidationError):
    def __init__(self, branch, branch_digit):
        branch_info = branch
        if branch_digit:
            branch_info += '-{}'.format(branch_digit)

        message = 'Branch "{}" is wrong.'.format(branch_info)
        super(InvalidBranch, self).__init__(message)


class InvalidAccount(BaseBankAccountValidationError):
    def __init__(self, account, account_digit):
        account_info = account
        if account_digit:
            account_info += '-{}'.format(account_digit)

        message = 'Account "{}" is wrong.'.format(account_info)
        super(InvalidAccount, self).__init__(message)


class InvalidBranchAndAccountCombination(BaseBankAccountValidationError):
    def __init__(self, branch, branch_digit, account, account_digit):
        branch_info = branch
        if branch_digit:
            branch_info += '-{}'.format(branch_digit)

        account_info = account
        if account_digit:
            account_info += '-{}'.format(account_digit)

        message = (
            'Combination (branch="{}", account="{}") does not match.'
        ).format(branch_info, account_info)
        super(InvalidBranchAndAccountCombination, self).__init__(message)
