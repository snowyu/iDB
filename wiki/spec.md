# iDB Specification

Version: 0.1

## Key

Key is always a directory.

## Value

The Value is a file or directory. It must be started with "=".
It must be '.value' name if cache the value to speed up.

the blob value in the cache file is the real blob file name link.

And it can be set to update to the cache file only for simple type.


## Root Dir

* .db/  Store the database meta infomation
  * version  Store the iDB Specification Version

## Value Type Descriptor

the ".type" directory in the key directory is the value type descriptor.

It's an optional item.


## Value Type

* Integer: 0..9 Number, eg, 421
* Hex: started with '$', eg, $4D1F
* Float
* Boolean: true/false, yes/no
* String: quoted with '"', or "'"
* Identifier: started with a letter and [\w]+

## Examples


    mydb/
        .db/.type/=object
        .db/version/=0.1
        .db/version/.type/=number


