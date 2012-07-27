#!/usr/bin/python
#coding:utf-8

import pytest
import unittest
from os import path
from idb.utils import RandomString
from shutil import rmtree
from idb.helpers import CreateDBString, GetFileValue, GetDBValue

ROOT_DIR = './mytestdb'
FIXTURE_DIR = path.join(path.realpath(__file__), 'fixtures')

def RandomKeyValue():
    key = RandomString()
    value = RandomString(26)
    return {'key': key, 'value': value}

def RandomPairs(aSize = 99):
    return [RandomKeyValue() for x in range(aSize)]

def create_pairs(aSize = 99, aCached = True):
    pairs = RandomPairs(aSize)
    for item in pairs:
        vDir = path.join(ROOT_DIR, item['key'])
        vStr = item['value']
        CreateDBString(vDir, vStr, aCached)
    return pairs

def check_pairs(pairs, wanted_result = True):
    for item in pairs:
        vDir =  path.join(ROOT_DIR, item['key'])
        vWantedStr = '=' + item['value']
        vStr = GetFileValue(vDir)
        assert len(vStr) == 1
        vStr = vStr[0]
        assert vStr == vWantedStr 

class BaseTest(unittest.TestCase):
    def setUp(self):
        rmtree(ROOT_DIR,  True)
    def tearDown(self):
        rmtree(ROOT_DIR, True)

