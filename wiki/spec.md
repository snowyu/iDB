# iDB Specification

Version: 2

the key base on a special urlencode.
the value only for file name base on a special urlencode.

* key's SafeChars(DO NOT ESCAPED CHARS): [/,' ']
* value's SafeChars: [' ']

## Key

Key is always a directory.

## Value

the value is the xattr of the directory. The content of the value must be started with "=".
the '.value' file will be exists in the same directory if backup enabled.

the blob value in the cache file is a blob file name link.(maybe I can use the real symbol link?)

And it can be set to update to the cache file only for simple type.


## DB Meta Infomation (Root Dir)

* .db/  Store the database meta infomation in the database root path.
  * version:Integer  the iDB Specification Version.
  * config:Object    the DB Configration (can be overload via application)
    * loadOnDemand:Boolean
    * storeInFile:Boolean
    * storeInXattr:Boolean
    * pageSize: Integer  the max size of a page.
    * raiseError:Object
      * typeMissMatch:Boolean

## Value Type Descriptor

* the ".type" is the value type descriptor for the key.
* the ".value" is the value's content for the key if any.
* the ".version" is the value type spec version if any.
* the ".keys" is the collection of keys in the current level(Dict) if any. 
  * Spec v1: the key list in the dict. seperate by "\n" (optional)
  * Spec v2: the key and type list in the dict. seperate by "\n" (optional)
    * key:type\n

## Value Type

* Integer: 0..9 Number, eg, 421
  * .type: Integer
  * .value: 12345
* Hex: started with '$' or '0x', eg, $4D1F
  * .type: Hex
  * .value: $2F01
* Float: the real number, eg, 3.1415
  * .type: Float
  * .value: 3.13
* Boolean: true/false, yes/no
  * .type: Boolean
  * .value: true
* String: quoted with '"', or "'" (quoted is optional)
  * .type: String
  * .value: "hi woold"
* Identifier: started with a letter and [\w\/]+
  * .type: 'Identifier'
  * .value: users/Mike
* Blob/XXX: XXX is the MIME type.
  * .type: Blob/Jpeg
  * .value: myphoto.jpg (the file name in this directory.)
* Dict: 
  * .type: Dict
  * .count: (if it's size is too large) (optional)
  * .level: (if it's size is too large) (optional)
  * .value: cache the dict's value if it's size is not too large. (optional)
  * .keys: the keys list of the dict. seperate by "\n" (optional)
* Object<Dict>: the object must have a uniqueue id in the same list.
  * .type:  Object
  * .value  cache the object data. (optional)
  * .keys   collects the property names of this object, seperate by "\n". (optional)
* List<Dict>: the keys is numbers from 0..count-1
  * .type: List
  * .count(if it's size is too large)
  * .level(if it's size is too large)
  * .value: a item each line if it's size is not too large (optional)
* Table<Dict>: the Item in Table is always the same type.
  * .type: Table
  * .fields  the fields and types of this table defined here.
  * .count(if it's size is too large)
  * .level(if it's size is too large)
  * .value: a item each line if it's size is not too large (optional)

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

## Expires(v2 Optional)

You can set a timeout on a key. After the timeout has expired, the key will automatically be deleted. A key with an associated timeout is often said to be volatile. The timeout is cleared only when the key is removed using the DEL command or overwritten using the SET/PUT commands.

Normally iDB keys are created without an associated time to live. The key will simply live forever, unless it is removed by the user in an explicit way, for instance using the DEL command.

* ".expires" the keys expiring information is stored as absolute Unix timestamps (in milliseconds). This means that the time is flowing even when the iDB instance is not active.

Optmal: Add expires index to .db.

## Index(v3)

## Version(v4)

## Examples

    mydb/
        .db/.type                    # this cached file's content is "Object"
        .db/version/.value           # this cached file's content is "0.1"
        .db/version/.type            # this cached file's content is "Float"
        mydict/.type                 # "Dict"
               .keys                 # "mystr\nmyobj"
               .value                # "'hi world'\n{item:1}"
               mystr/.type           # "String"
                     .value          # "hi world"
               myobj/.type           # "Object"
                     item/.type      # "Integer"
                          .value     # "1"

        users/.type                  # "Table:Object/User"
        users/.keys                  # "Mike\nRose"
        users/.value                 # "{name:"Mike Jones", sex:"Male"}\n..."
        users/Mike/.type             # "Object/User"
        users/Mike/.keys             # the field names: "name\nsex"
        users/Mike/.value            # {name:"Mike Jones", sex:"Male"}
        users/Mike/name/.type        # "String"
        users/Mike/name/.value       # "'Mike Jones'"
        users/Mike/sex/.value        # "Male"
        users/Rose/

