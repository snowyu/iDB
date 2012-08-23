## iDB Value Types Prototype


### iDBValue Abstract Class

* Manage the ValueType Classes

Class iDBValue(Object):
  Constructor Create(const aDB: iDB);
  Class Method Register(const aType: iDBValue): Boolean;
  Class Method UnRegister(const aType: iDBValue): Boolean;
  Class Method Types: List;
  Class Method[Virtual] Save(const aDB: iDB; const aKey: String): Boolean;
  Class Method[Virtual] Load(const aDB: iDB; const aKey: String): Boolean;
  Method Save(const aKey: String): Boolean;
  Method Load(const aKey: String): Boolean;
  Property database: iDB;
  Property asString: String;
  Property valueType: String;

### String(iDBValue) Class

### Numberic(iDBValue) Abstract Class

### Dict(iDBValue) Class

## iDB Class Prototype


### Methods

* Class Method New(path="", loadOnDemand=True, storeInFile=True, storeInXattr=False, opened=False): iDB;
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
* Method iGetValue(const aKey: String): String;
  * Internal Get the value of aKey as string.
* Method iGetType(const aKey: String): String;
  * Internal Get the value type of aKey
* Method iPut(const aKey: String, const aValue: String, const aType: String): String;
  * Internal save the value and value type of aKey as string.
* Method iDelete(const aKey: String): Boolean;
  * Internal delete the key directly.
* Method iGetDict(const aKey: String): Dict;
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

