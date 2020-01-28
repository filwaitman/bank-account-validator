# -*- coding: utf-8 -*-
import re


def smarter_zfill(value, expected_length=None):
    if not value:
        return ''

    result = re.sub('^0+', '', str(value))

    if expected_length:
        result = result.zfill(expected_length)

    return result


def calculate_verifier_digit(
    account_relevant_data, pivot, method='mod11', sum_digits=False
):
    def _sum_digits(value):
        return sum([int(x) for x in str(value)])

    if len(account_relevant_data) != len(pivot):
        raise RuntimeError('Invalid method: {}'.format(method))

    values = [
        int(x) * int(y)
        for x, y in zip(account_relevant_data.zfill(len(pivot)), pivot)
    ]

    result = sum(values)
    if sum_digits:
        result = sum([_sum_digits(x) for x in values])

    if method == 'mod10':
        result = 10 - (result % 10)
    elif method == 'mod11':
        result = 11 - (result % 11)
    else:
        raise RuntimeError('Invalid method: {}'.format(method))

    return result
