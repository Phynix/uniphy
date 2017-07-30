#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 13:29:21 2017

@author: johannes
"""

import pickle
import os
import decorators

class Wallet:
    maxID = 0

    @decorators.type_checked
    def __init__(self, name: str=None, entries: list=None):
        self.id = self.maxID
        type(self).maxID += 1

        if name is None:
            name = 'wallet{}'.format(self.id)
        if entries is None:
            entries = []

        self.name = name
        self.entries = entries
        self.dir = '.'

    @property
    def file(self):
        return '{}/{}'.format(self.dir, self.name)

    def save(self, file=None):
        if file is None:
            file = self.file
            if not os.path.isdir(self.dir):
                os.makedirs(self.dir)
        with open(file, 'wb') as ofile:
            pickle.dump(self.entries, ofile)

    def load(self, file=None):
        if file is None:
            file = self.file
        with open(file, 'rb') as ifile:
            self.entries = pickle.load(ifile)
