#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 13:51:04 2017

@author: johannes
"""

import unittest
from wallet import Wallet


class WalletTest(unittest.TestCase):

    pass


if __name__ == '__main__':
    wallet = Wallet('hello', 'hello')
    wallet.save()
    print(wallet.entries)
