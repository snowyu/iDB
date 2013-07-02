# idb specification

Version: 2


## Key

The maximum key name length is 255 bytes.

* the key name do not allow begin with "."

## Value

The most import attribute is the **value** of a key.

the value is the xattr of the directory.
the '.value' file will be exists in the same directory if backup enabled.

the blob value in the cache file is a blob file name link.(maybe I can use the real symbol link?)

And it can be set to update to the cache file only for simple type.

### Value Format

the value format should be binary or text, It's defined via the db meta infomation.

#### Text

the text is always utf-8 string.

总觉得没有必要支持binary形式的格式，只要纯文本即可。
可以在内存中使用binary，而保存在磁盘的总是纯文本。

#### binary

Integer, Float: Little-Endian

IMPL: redis/src/endianconv.h

   * intrev16ifbe: convert unsigned int16 if target host is big-endian.
   * memrev32ifbe: convert single float if target host is big-endian.
   * memrev64ifbe: covert double folat if target host is big-endian.

BigInt, BigFloat: [GMP Library](http://gmplib.org/)

DateTime: [ISO8601](http://www.iso.org/iso/date_and_time_format) String
    20081022T234350Z ： 表示格林威治时间2008年10月22号23点43分50秒

String: UTF-8


## iDB Meta Infomations (Root Dir)

* .db/  Store the database meta infomation in the database root path.
  * version:Integer  the iDB Specification Version.
  * format: String   the value format of this iDB. It should be binary, text(utf-8)
                     the database meta informations are always text.
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

## Simple Type

* Integer: 0..9 Number, eg, 421
  * .type: Single/Integer
  * .value: 12345
   started with '$' or '0x' means hex base, eg, $4D1F
   started with '0' means octal base, eg, 017
   //started with '0b' means bin base, eg, 0b0011011
* Float: the real number, eg, 3.1415
  * .type: Single/Float
  * .value: 3.13
* Boolean: true/false, yes/no
  * .type: Single/Boolean
  * .value: true
* String: quoted with '"', or "'" (quoted is optional)
  * .type: Single/String
  * .value: "hi woold"
* Identifier: started with a letter and [\w\/]+
  * .type: Single/Identifier
  * .value: users/Mike
* Blob/XXX: XXX is the MIME type.
  * .type: Single/Blob/Jpeg
  * .value: myphoto.jpg (the file name in this directory.)

## Complex Type

### Collection(List) Type

考虑到非常大集合的情况，我们采用了分页方式(Pagination)
* pageSize
* level 当前所在分页层级(如果该属性不存在，则默认为0层级－未分页)

为了加速访问，可以采用Cache机制，
以下属性就是为加速读访问而设置的:

* count 总数
  如果没有，那么计算方法如下: 
  * 遍历所有目录，检查目录的值类型
    * Single Type 值类型是简单类型:
      * count+=1
    * List Type:
      * count+=1 if level=0
      * count+=1 if 存在目录(.me)


#### IndexDB Internal Mechanism

IndexDB由若干排序文件(IndexFile)组成，每一文件又由若干排序块(IndexBlock)组成。
排序块由若干排序Key/Value记录项(定长IndexItem)构成。
文件所容纳的排序块数是固定的。排序块所容纳的记录条数也
是固定的。

排序文件头中记录了该文件的最大Key是哪一个，以及记录条数，和各个块的使用情况。
块也会记录该块中的最大key是哪一个.

##### 操作

查记录key所在位置(应该在哪里插入),

* 遍历 IndexFile 的信息, IndexFile 的信息递增存放, 获取该key所在哪一文件,然后在获取该key在哪一个块上。

        int GetIndexFileId(char *aKey) {
            int i;
            for (i=0; i < darray_size(indexes); i++) {
                //aKey <= indexes[i].maxKey
                if (strcmp(aKey, darray_item(indexes, i).maxKey) <= 0)
                    return i;
            }
            //aKey > all indexes.maxKey
            i--;
            return i;
        }
        int iIndexFile_GetBlockId(IndexFile *self, char *aKey) {
            int i;
            for (i = 0; i < darray_size(blocks); i++) {
                //aKey <= blocks[i].maxKey
                if (strcmp(aKey, darray_item(blocks, i).maxKey) <= 0)
                    return i;
            }
            //aKey > all blocks.maxKey
            i--;
            return i;
        }


Set(aKey, aValue):

如果cache满了，那么交换cache和cacheSaving，并在后台开始保存cacheSaving(保存完毕后将cacheSaving清空).
然后添加到cache上。

保存流程:

    iIndexDB_SaveItems(aItems) {
        for (i = 0; i < darray_size(aItems); i++) {
            iIndexDB_SaveItem(darray_item(aItems, i));
        }
    }
    iIndexDB_SaveItem(aItem) {
        int i;
        IndexFile *vIndexFile = GetIndexFile(aItem.key);
        iIndexFile_SaveItem(aItem);
    }
    iIndexFile_GetBlock(IndexFile *self, aItem) {
    }
    iIndexFile_SaveItem(IndexFile *self, aItem) {
        if dd
        IndexBlock *vBlock = iIndexFile_GetBlockByKey(IndexBlock *self, char *aKey);
    }

#### 索引

所有的索引存放在键的 ".index" 目录（可以视作为一个特殊的子键）里面。
其中 ".index/.keys" 目录里面为对子健的索引，这是系统默认索引，总是存在。


* .index/.keys 保存所有的Key名称(仅当level=0时候才存在), key名称是递增排
  序的，key之间用"\n"分隔.如果keys超过最大限制(LimitedSize)，那么分
  多个文件保存，将原来的keys文件改名为keys.0, 后续文件命名为:
  keys.1, ..., keys.n，并增加 keys.index 文件，记录每一个keys.n
  文件中的最后一个key，同样用"\n"分隔.
  * keys.n 文件格式: <Key Name>\t<Key Path>\n
  * keys.index 文件格式, 行号就对应了keys.n: <Last Key Name>\n

排序文件扩展名的修改：改序列数字n为带层级的排序标示，比如：keys.1 keys.a
表示小于等于1的keys存放在keys.1中，大于1并且小于等于“a”（即含a以及a到1之间的）
的keys存放在keys.a文件中。
如果keys.a满了（达到最大的存储限制），那么创建目录".keys.a"，存放：
keys.a1, keys.aa 等等诸如此类。


index文件格式如下：最后决定还是binary格式，因为定长才好随机读取。

Key[MaxKeySize] Offset length
offset 为在文件中的偏移量。
如果长度length为0表示，没有分区，key名就是直接读取的位置。

保留一定区域的定长记录，可以分成4份,第一份为 0 Level, 2为 1 Level, n 为 n Level
一个比一个长，那么一份总共可以记录的条数 = 4^n * BlockGap
首先往 0 Level里面塞，塞满了，往 Level 1塞，记住 Level 1以后里面的全部是排好序的。
只有Level 0 是没有排序的。

如果4份全部填满了。那么新开3个文件，将其中的4分之3都移走，这样每一个文件都有1/4。

	L = sst_in_one(node->sst, &c); //以排好序的形式从磁盘取出

	//NESSDB_SST_SEGMENT 总共分的4个文件(含自身)。
    split = c / NESSDB_SST_SEGMENT; //每份的项数
	mod = c % NESSDB_SST_SEGMENT;
	k = split + mod; //得到切分点,

在内存中记录各个index文件的数组称为: meta.nodes[3000] 固定3000个

    nxt_idx = _get_idx(meta, L[k - 1].data) + 1; //取得L[k-1] key应该在哪一个index文件的在meta数组中的idx.


Collection(List)类型的操作除了有GetAll之外，还有GetByPattern(Find)
当不存在keys文件的时候，Get的操作如下：
  * 遍历所有目录，检查目录的值类型
    * Single Type 值类型是简单类型:
      * add to list if pattern matched
    * 如果是List Type:
      * add to list if level=0 and pattern matched
      * add to list if 存在目录(.me) and pattern matched




* Dict: 
  * .type: List/Dict
  * .count: (if it's size is too large) (optional)
  * .level: (if it's size is too large) (optional)
  * .value: cache the dict's value if it's size is not too large. (optional)
  * .keys: the keys list of the dict. seperate by "\n" (optional)
* Object<Dict>: the object must have a uniqueue id in the same list.
  * .type:  List/Object
  * .value  cache the object data. (optional)
  * .keys   collects the property names of this object, seperate by "\n". (optional)
* List<Dict>: the keys is numbers from 0..count-1
  * .type: List
  * .count(if it's size is too large)
  * .level(if it's size is too large)
  * .value: a item each line if it's size is not too large (optional)
* Table<Dict>: the Item in Table is always the same type.
  * .type: List/Table
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

优化： 可以在.db中增加一个目录保存所有的非持久性keys（有到期时间的），将它们按照到期时间组织，一次性清理。这个有点类似索引，可以考虑索引的方式。

## Index(v3)
=======
Optimal: Add expires index to .db.

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

    * List Type:
# iDB Specification
