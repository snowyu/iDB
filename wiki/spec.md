# iDB Specification

Version: 0.2

the key base on a special urlencode.
the value only for file name base on a special urlencode.

* key's SafeChars: [/,' ']
* value's SafeChars: [' '] 

## Key

Key is always a directory.

## Value

the value is the xattr of the directory. The content of the value must be started with "=".
the '.value' file will be exists in the same directory if backup enabled.

the blob value in the cache file is a blob file name link.(maybe I can use the real symbol link?)

And it can be set to update to the cache file only for simple type.


## Root Dir

* .db/  Store the database meta infomation in the database root path.
  * version  Store the iDB Specification Version

## Value Type Descriptor

the ".type" is the value type descriptor for the key.

## Value Type

* Integer: 0..9 Number, eg, 421
* Hex: started with '$' or '0x', eg, $4D1F
* Float: the real number, eg, 3.1415
* Boolean: true/false, yes/no
* String: quoted with '"', or "'"
* Identifier: started with a letter and [\w]+
* Blob/XXX: XXX is the MIME type.
  * .value: the file name in this directory.
* Dict: 
  * .value: cache the dict's value if it's size is not too large. (optional)
  * .fields: the keys list of the dict. seperate by "\n" (optional)
* Object<Dict>: the object must have a uniqueue id in the same list.
-  * .value  cache the object data. (optional)
-  * .fields collects the property names of this object, seperate by "\n". (optional)
* List<Dict>: the keys is numbers from 0..count-1
  * .count
  * .level
  * .value: a item each line(only id for the object item) (optional)

* Item(Abstract):
  * Numberic(Abstract):
    * Hex
    * Integer
    * Float
  * String
  * Dict
    * Object
    * List
    * PagedDict
      * PagedList


