## iDB Value Types Prototype

* String
  * Integer
  * Hex
  * Boolean
  * Float
* Dict
* List(Array)

## iDB Class Prototype


### Methods

* Class Method New(path="", loadOnDemand=True, storeInFile=True, storeInXattr=False, opened=False, raiseError=[reTypeMissMatch]): iDB;
  * Create a new iDB object instance.
  * Parameters(Optional):
    * path: the database path
    * loadOnDemand: the default is True.
    * storeInFile:  the default is True.
    * storeInXattr: the default is True.
    * opened: whether open the database after new(the path MUST be setting if true). the default is False.
* Method Open(skipDBConfig=False): Boolean;
  * Open a iDB database, the property path MUST BE setting first.
  * Parameters(Optional):
    * skipDBConfig: whether skip to load the dbconfig from database. the default is False.
* Method Close();
  * Close a iDB database.
* Method iGetValueAndType(const aKey: String): Dict;
  * Internal Get the value and type of aKey as string.
  * return : {value:"", type:""}
* Method iGetValue(const aKey: String): String;
  * Internal Get the value of aKey as string.
* Method iGetType(const aKey: String): String;
  * Internal Get the value type of aKey
* Method iGetDict(const aKey: String): Dict;
* Method iPut(const aKey: String, const aValue: String, const aType: String): String;
  * Internal save the value and value type of aKey as string.
* Method iDelete(const aKey: String): Boolean;
  * Internal delete the key directly.
* Method Get(const aKey: String): Variant;

### Properties

* path: string
* storeInFile: Boolean
* storeInXattr: Boolean
* loadOnDemand: Boolean
* opened: Boolean
  * the database whether is opened.
* version: String
  * the database specification version
* raiseError: Set
  * reTypeMissMatch: Bit0

