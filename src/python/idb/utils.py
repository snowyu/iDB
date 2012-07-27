#!/usr/bin/python
#coding:utf-8

import string, random
import os
import errno


def RandomString(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

# Create all missed directoy 
def CreateDir(aDir):
    try:
        os.makedirs(aDir)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def TouchFile(aFileName, aTimeStamp = None):
    #fhandle = 
    file(aFileName, 'a').close()
    if aTimeStamp != None:
        try:
            os.futimes(aFileName, aTimeStamp)
        except ENOSYS:
            os.utime(aFileName, aTimeStamp)
        #finally:
        #    fhandle.close()

# the Conversion functions:
def Str2Hex(value):
    if value[0]  == '$':
        value = value[1:]
    return int(value, 16)

def Hex2Str(value):
    return '$' + hex(value)[2:]

def Str2Bool(value):
    """
    Converts 'something' to boolean. Raises exception if it gets a string it doesn't handle.
    Case is ignored for strings. These string values are handled:
      True: 'True', "TRue", "yes", "y", "t"
      False: "", "faLse", "no", "n", "f"
    #Non-string values are passed to bool.
    """
    #if type(value) == type(''):
    if value.lower() in ("yes", "y", "true",  "t", ):
        return True
    if value.lower() in ("no",  "n", "false", "f"):
        return False
    raise ValueError('Invalid value for boolean conversion: ' + value)
    #return bool(value)

