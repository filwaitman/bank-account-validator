# -*- coding: utf-8 -*-
import unittest

from bank_account_validator.core import BrazilianBank
from bank_account_validator.exceptions import (
    BankNotImplemented, InvalidBranch, InvalidAccount, InvalidBranchAndAccountCombination, InvalidBranchlength,
    InvalidAccountlength, MissingBranchDigit, MissingAccountDigit, UnexpectedBranchDigit, UnexpectedAccountDigit
)
from tests.data import BANRISUL, BANCO_DO_BRASIL, SANTANDER, CAIXA_ECONOMICA_FEDERAL, BRADESCO, ITAU


class BanrisulValidateBranchDigitTestCase(unittest.TestCase):
    def test_common(self):
        for branch, expected_dv in BANRISUL['correct_data']:
            self.assertTrue(
                BrazilianBank.get('041')(
                    branch=branch,
                    branch_digit=expected_dv,
                    account='1',
                    account_digit='1'
                ).validate_branch_digit()
            )


class BankAccountValidatorBaseTestCase(object):
    def test_valid_accounts(self):
        errors = []
        for bank_data in self.valid_combinations:
            try:
                BrazilianBank.get(bank_data['bank_code'])(
                    branch=bank_data['branch'],
                    branch_digit=bank_data['branch_digit'],
                    account=bank_data['account'],
                    account_digit=bank_data['account_digit']
                ).execute()
            except (InvalidBranch, InvalidAccount, InvalidBranchAndAccountCombination):
                errors.append(bank_data)

        if errors:
            msg = '{} accounts were not successfully validated.'.format(len(errors))
            for error in errors:
                msg += "\naccount_number_validator('{}', '{}', '{}') returned False (expected True)".format(*error)

            self.fail(msg)

    def test_invalid_accounts(self):
        errors = []
        for bank_data in self.invalid_combinations:

            try:
                BrazilianBank.get(bank_data['bank_code'])(
                    branch=bank_data['branch'],
                    branch_digit=bank_data['branch_digit'],
                    account=bank_data['account'],
                    account_digit=bank_data['account_digit']
                ).execute()

                errors.append(bank_data)
            except (InvalidBranch, InvalidAccount, InvalidBranchAndAccountCombination):
                pass  # that's the expected scenario - just like an assertRaises for multiple exceptions

        if errors:
            msg = '{} accounts were not successfully validated.'.format(len(errors))
            for error in errors:
                msg += "\naccount_number_validator('{}', '{}', '{}') returned True (expected False)".format(*error)

            self.fail(msg)


class BancoDoBrasilTestCase(BankAccountValidatorBaseTestCase, unittest.TestCase):
    valid_combinations = BANCO_DO_BRASIL['valid_combinations']
    invalid_combinations = BANCO_DO_BRASIL['invalid_combinations']


class SantaderTestCase(BankAccountValidatorBaseTestCase, unittest.TestCase):
    valid_combinations = SANTANDER['valid_combinations']
    invalid_combinations = SANTANDER['invalid_combinations']


class CaixaEconomicaFederalTestCase(BankAccountValidatorBaseTestCase, unittest.TestCase):
    valid_combinations = CAIXA_ECONOMICA_FEDERAL['valid_combinations']
    invalid_combinations = CAIXA_ECONOMICA_FEDERAL['invalid_combinations']


class BradescoTestCase(BankAccountValidatorBaseTestCase, unittest.TestCase):
    valid_combinations = BRADESCO['valid_combinations']
    invalid_combinations = BRADESCO['invalid_combinations']


class ItauTestCase(BankAccountValidatorBaseTestCase, unittest.TestCase):
    valid_combinations = ITAU['valid_combinations']
    invalid_combinations = ITAU['invalid_combinations']


class PreconditionExceptionsTestCase(unittest.TestCase):
    def setUp(self):
        super(PreconditionExceptionsTestCase, self).setUp()

        self.valid_data = {
            'branch': '1769',
            'branch_digit': '8',
            'account': '200040',
            'account_digit': '7',
        }

        self.bank = BrazilianBank.get('237')

    def test_not_implemented_bank(self):
        with self.assertRaises(BankNotImplemented) as e:
            BrazilianBank.get(999)
        self.assertEquals(e.exception.message, 'Bank code "999" is not implemented for country "BR"- or it does not exist at all.')

    def test_missing_digit_on_branch(self):
        self.valid_data['branch_digit'] = ''

        with self.assertRaises(MissingBranchDigit) as e:
            self.bank(**self.valid_data)
        self.assertEquals(e.exception.message, 'For bank code "237", branches must have a digit, of length 1.')

    def test_unexpected_branch_digit(self):
        self.valid_data['branch_digit'] = '12'

        with self.assertRaises(UnexpectedBranchDigit) as e:
            self.bank(**self.valid_data)
        self.assertEquals(e.exception.message, 'For bank code "237", branches must have 1 digits.')

    def test_missing_digit_on_account(self):
        self.valid_data['account_digit'] = ''

        with self.assertRaises(MissingAccountDigit) as e:
            self.bank(**self.valid_data)
        self.assertEquals(e.exception.message, 'For bank code "237", accounts must have a digit, of length 1.')

    def test_unexpected_account_digit(self):
        self.valid_data['account_digit'] = '12'

        with self.assertRaises(UnexpectedAccountDigit) as e:
            self.bank(**self.valid_data)
        self.assertEquals(e.exception.message, 'For bank code "237", accounts must have 1 digits.')

    def test_branch_too_big(self):
        self.valid_data['branch'] = '17695'

        with self.assertRaises(InvalidBranchlength) as e:
            self.bank(**self.valid_data)
        self.assertEquals(e.exception.message, 'For bank code "237", branches length must be 4.')

    def test_account_too_big(self):
        self.valid_data['account'] = '12000408'

        with self.assertRaises(InvalidAccountlength) as e:
            self.bank(**self.valid_data)
        self.assertEquals(e.exception.message, 'For bank code "237", accounts length must be 7.')

    def test_zeroes_at_left_doesnt_count(self):
        self.valid_data['branch'] = '000000001768'
        self.valid_data['account'] = '00000200040'
        self.bank(**self.valid_data)  # nothing has raised


class InvalidAccountExceptionsTestCase(unittest.TestCase):
    def test_invalid_branch_digit(self):
        data = {
            'bank_code': '237',
            'branch': '1769',
            'branch_digit': '1',  # should be '8'
            'account': '200040',
            'account_digit': '7',
        }

        with self.assertRaises(InvalidBranch) as e:
            BrazilianBank.get(data['bank_code'])(**data).execute()
        self.assertEquals(e.exception.message, 'Branch "1769-1" is wrong.')

    def test_invalid_account_digit(self):
        data = {
            'bank_code': '237',
            'branch': '1769',
            'branch_digit': '8',
            'account': '200040',
            'account_digit': '1',  # should be '7'
        }

        with self.assertRaises(InvalidAccount) as e:
            BrazilianBank.get(data['bank_code'])(**data).execute()
        self.assertEquals(e.exception.message, 'Account "0200040-1" is wrong.')

    def test_invalid_branch_account_combination(self):
        data = {
            'bank_code': '033',
            'branch': '2006',
            'branch_digit': '',
            'account': '01008407',
            'account_digit': '1',  # should be '4'
        }

        with self.assertRaises(InvalidBranchAndAccountCombination) as e:
            BrazilianBank.get(data['bank_code'])(**data).execute()
        self.assertEquals(e.exception.message, 'Combination (branch="2006", account="01008407-1") does not match.')
