# -*- coding: utf-8 -*-
import unittest

from bank_account_validator.utils import smarter_zfill


class SmarterZfillTestCase(unittest.TestCase):
    def test_common_zfill(self):
        self.assertEqual(smarter_zfill('1', 4), '0001')

    def test_remove_leading_zeroes(self):
        self.assertEqual(smarter_zfill('0000000000001', 4), '0001')

    def test_integer(self):
        self.assertEqual(smarter_zfill(1, 4), '0001')

    def test_empty_string(self):
        self.assertEqual(smarter_zfill('', 4), '')

    def test_None(self):
        self.assertEqual(smarter_zfill(None, 4), '')

    def test_if_expected_length_is_None_just_remove_leading_zeroes(self):
        self.assertEqual(smarter_zfill('0000000000001'), '1')
