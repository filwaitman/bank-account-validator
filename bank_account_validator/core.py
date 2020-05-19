# -*- coding: utf-8 -*-
from bank_account_validator.exceptions import (
    BankNotImplemented, InvalidBranch, InvalidAccount, InvalidBranchAndAccountCombination, InvalidBranchlength,
    InvalidAccountlength, MissingBranchDigit, MissingAccountDigit, UnexpectedBranchDigit, UnexpectedAccountDigit
)
from bank_account_validator.utils import smarter_zfill, calculate_verifier_digit


def all_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in all_subclasses(s)]


class Bank(object):
    country = None
    bank_code = None

    branch_length = 4
    branch_digit_length = 0

    account_length = 10
    account_digit_length = 1

    def __init__(self, **kwargs):
        if not all([self.country, self.bank_code]):
            raise RuntimeError('Bank is an abstract class and must not be instantiated. '
                               'Use its subclasses instead - via Bank.get(bank_code, country).')

        self.branch = smarter_zfill(kwargs['branch'], self.branch_length)
        self.branch_digit = smarter_zfill(kwargs.get('branch_digit', ''), self.branch_digit_length)
        self.account = smarter_zfill(kwargs['account'], self.account_length)
        self.account_digit = smarter_zfill(kwargs.get('account_digit', ''), self.account_digit_length)

        if len(self.branch) != self.branch_length:
            raise InvalidBranchlength(self)

        if len(self.branch_digit) < self.branch_digit_length:
            raise MissingBranchDigit(self)

        if len(self.branch_digit) > self.branch_digit_length:
            raise UnexpectedBranchDigit(self)

        if len(self.account) != self.account_length:
            raise InvalidAccountlength(self)

        if len(self.account_digit) < self.account_digit_length:
            raise MissingAccountDigit(self)

        if len(self.account_digit) > self.account_digit_length:
            raise UnexpectedAccountDigit(self)

    @classmethod
    def get(cls, bank_code, country=None):
        if not country:
            country = cls.country

        subclasses = all_subclasses(cls)
        bank_class = list(filter(lambda x: x.bank_code == bank_code and x.country == country, subclasses))

        if bank_class:
            return bank_class[0]
        raise BankNotImplemented(bank_code, country)

    def validate_branch_digit(self):
        return True

    def validate_account_digit(self):
        return True

    def validate(self):
        return True

    def execute(self):
        if not self.validate_branch_digit():
            raise InvalidBranch(self.branch, self.branch_digit)

        if not self.validate_account_digit():
            raise InvalidAccount(self.account, self.account_digit)

        if not self.validate():
            raise InvalidBranchAndAccountCombination(self.branch, self.branch_digit, self.account, self.account_digit)


class BrazilianBank(Bank):
    country = 'BR'


class BancoDoBrasil(BrazilianBank):
    bank_code = '001'
    account_length = 8
    branch_digit_length = 1

    def validate_branch_digit(self):
        s = sum(int(x) * y for x, y in zip(list(self.branch), range(5, 1, -1)))
        remaining_part = s % 11

        dv = 11 - remaining_part
        if remaining_part == 0:
            dv = 0
        elif remaining_part == 1:
            dv = 'x'

        return self.branch_digit.lower() == str(dv).lower()

    def validate_account_digit(self):
        dv = calculate_verifier_digit(self.account, pivot='98765432')
        dv = 'X' if dv == 10 else dv
        dv = '0' if dv == 11 else dv

        return self.account_digit.lower() == str(dv).lower()


class Santander(BrazilianBank):
    bank_code = '033'
    account_length = 8

    def validate(self):
        account_relevant_data = self.branch + '00' + self.account
        dv = calculate_verifier_digit(account_relevant_data, pivot='97310097131973', method='mod10')
        dv = '0' if dv == 10 else dv

        return self.account_digit.lower() == str(dv).lower()


class Banrisul(BrazilianBank):
    bank_code = '041'
    branch_digit_length = 2
    account_length = 9
    # TODO: tests for account validation

    def validate_branch_digit(self):
        def sum_digits(value):
            return sum([int(x) for x in str(value)])

        first_digit = 10 - ((sum_digits(int(self.branch[0]) * 1) +
                             sum_digits(int(self.branch[1]) * 2) +
                             sum_digits(int(self.branch[2]) * 1) +
                             sum_digits(int(self.branch[3]) * 2)) % 10)

        if first_digit == 10:
            first_digit = 0

        second_digit = 11 - ((int(self.branch[0]) * 6 +
                              int(self.branch[1]) * 5 +
                              int(self.branch[2]) * 4 +
                              int(self.branch[3]) * 3 +
                              first_digit * 2) % 11)

        if second_digit == 11:
            second_digit = 0
        elif second_digit == 10:
            first_digit = (first_digit + 1) % 10
            second_digit = 11 - ((int(self.branch[0]) * 6 +
                                  int(self.branch[1]) * 5 +
                                  int(self.branch[2]) * 4 +
                                  int(self.branch[3]) * 3 +
                                  first_digit * 2) % 11)

        return self.branch_digit.lower() == '{}{}'.format(first_digit, second_digit).lower()

    def validate_account_digit(self):
        dv = calculate_verifier_digit(self.account, pivot='324765432')
        dv = '6' if dv == 10 else dv
        dv = '0' if dv == 11 else dv

        return self.account_digit.lower() == str(dv).lower()


class CaixaEconomicaFederal(BrazilianBank):
    bank_code = '104'
    account_length = 11

    def validate(self):
        account_relevant_data = self.branch + self.account
        pivot = '876543298765432'
        dv = sum([int(x) * int(y) for x, y in zip(account_relevant_data.zfill(len(pivot)), pivot)])
        dv *= 10
        dv %= 11
        dv = '0' if dv == 10 else dv

        return self.account_digit.lower() == str(dv).lower()


class Bradesco(BrazilianBank):
    bank_code = '237'
    account_length = 7
    branch_digit_length = 1

    def validate_branch_digit(self):
        s = sum(int(x) * y for x, y in zip(list(self.branch), range(5, 1, -1)))
        remaining_part = s % 11

        dv = 11 - remaining_part
        if remaining_part == 0:
            dv = 0
        elif remaining_part == 1:
            dv = 0

        return self.branch_digit.lower() == str(dv).lower()

    def validate_account_digit(self):
        dv = calculate_verifier_digit(self.account, pivot='2765432')
        dv = '0' if dv == 10 else dv  # according to documentation this one should be 'P', but I know this info is outdated
        dv = '0' if dv == 11 else dv

        return self.account_digit.lower() == str(dv).lower()


class Itau(BrazilianBank):
    bank_code = '341'
    account_length = 5

    def validate(self):
        account_relevant_data = self.branch + self.account
        dv = calculate_verifier_digit(account_relevant_data, pivot='212121212', sum_digits=True, method='mod10')
        dv = '0' if dv == 10 else dv

        return self.account_digit.lower() == str(dv).lower()


class HSBC(BrazilianBank):
    bank_code = '399'
    account_length = 6
    # TODO: tests

    def validate(self):
        account_relevant_data = self.branch + self.account
        pivot = '8923456789'
        dv = sum([int(x) * int(y) for x, y in zip(account_relevant_data.zfill(len(pivot)), pivot)])
        dv %= 11
        dv = '0' if dv == 10 else dv

        return self.account_digit.lower() == str(dv).lower()


class Citibank(BrazilianBank):
    bank_code = '745'
    account_length = 7
    # TODO: branch validation and tests

    def validate_account_digit(self):
        dv = calculate_verifier_digit(self.account, pivot='8765432')
        dv = '0' if dv == 10 else dv
        dv = '0' if dv == 11 else dv

        return self.account_digit.lower() == str(dv).lower()
