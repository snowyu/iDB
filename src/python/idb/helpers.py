#!/usr/bin/python
#coding:utf-8

import utils
import errno
import glob

from os import path
from shutil import rmtree

from utils import Str2Hex, Str2Bool, CreateDir, TouchFile

# Constants
# the iDB Library version:
IDB_VER = '0.0.1'
# the iDB Specification version:
IDB_SPEC_VER = '0.1'

IDB_KEY_TYPE = '.type'
IDB_VALUE_FILE = '=*'
IDB_VALUE_CACHE_FILE = '.value'
IDB_TYPES = {'string': str, 'object': dict, 'integer': int, 'hex': Str2Hex, 'float': float, 'boolean': Str2Bool}
IDB_LTYPES = {str: 'String', dict: 'Object', int: 'Integer', hex: 'Hex', float: 'Float', bool: 'Boolean'}

def GetFileValue(aDir):
    aFile = path.join(aDir, IDB_VALUE_CACHE_FILE)
    result = None
    try:
        result = [line.strip() for line in open(aFile, 'r')]
    except IOError, e:
        if e.errno != errno.ENOENT: # No Such File
            raise
    if result == None:
        aFile = path.join(aDir, IDB_VALUE_FILE)
        result = glob.glob(aFile) # Search dir by pattern
    return result

def CreateDBString(aDir, aString, aCached = True):
    """Create aString in aDir
    """
    aFile = path.join(aDir, '=' + aString)
    aDir = path.dirname(aFile)
    aString = path.basename(aFile)
    CreateDir(aDir)
    TouchFile(aFile)
    if aCached:
        aFile = path.join(aDir, IDB_VALUE_CACHE_FILE)
        with open(aFile, 'w') as f:
            f.write(aString)

# the helper functions to operate the iDB
def CreateDBValue(aDir,  aValue, aValueType):
    """
    """
def GetDBValue(aDir):
    vValues = GetFileValue(aDir) # Search dir by pattern
    if len(vValues) > 0:
        # load value into vValues now.
        vValues = [value.replace(path.join(aDir, '='),'') for value in vValues] #remove the prefix "="
        #for i, value in enumerate(vValues):
        #    vValues[i] = value.replace(path.join(aDir, '='),'')  #remove the prefix "="

        # try to determine the value's type.
        vKeyTypeDir = path.join(aDir, IDB_KEY_TYPE)
        vKeyType = None
        if path.exists(vKeyTypeDir):
            value = glob.glob(path.join(vKeyTypeDir, IDB_VALUE_FILE))
            if len(value) > 0:
                value = str.lower(value[0])
                if IDB_TYPES.has_key(value):
                    vKeyType = IDB_TYPES[value]
        if len(vValues) == 1:
            vValues = vValues[0]
            if vKeyType == None: # guess the type of the value
                if vValues[0] == '$':
                    try:
                        vValues  = int(vValues[1:], 16)
                        vKeyType = hex
                    except ValueError:
                        pass
                if vKeyType == None:
                    if (vValues[i][0]  == '"' and vValues[i][-1]  == '"'):
                        vValues[i] = vValues[1:-1]
                        vKeyType = str
                    elif (vValues[i][0]  == '\'' and vValues[i][-1]  == '\''):
                        vValues[i] = vValues[1:-1]
                        vKeyType = str

                if vKeyType == None:
                    try:
                        vValues  = int(vValues)
                        vKeyType = int
                    except ValueError:
                        pass
                if vKeyType == None:
                    try:
                        vValues  = float(vValues)
                        vKeyType = float
                    except ValueError:
                        pass
                if vKeyType == None:
                    try:
                        vValues = Str2Bool(vValues)
                        vKeyType = bool
                    except ValueError:
                        pass
                if vKeyType == None:
                    vKeyType = str
                    # remove quote if any
                    for i, value in enumerate(vValues):
                        if vValues[i][0]  == '"' and vValues[i][-1]  == '"':
                            vValues[i] = vValues[1:-1]
                        elif vValues[i][0]  == '\'' and vValues[i][-1]  == '\'':
                            vValues[i] = vValues[1:-1]

                CreateDBString(vKeyTypeDir, IDB_LTYPES[vKeyType])
            else:
                vValues = vKeyType(vValues)
        return vValues


