iDB - 下一代面向列结构化层级数据库(Structed-Column Oriented Hierarchy Database)
=========================================================================

iDB 是结构化的面向列层级数据存储系统，所谓面向列(Column)是和面向行(Row)相对
而言的，绝大多数的关系型数据库就是面向行存储的，而iDB则是面向列基于Key/Value
的存储系统，所谓结构化是指值(Value)可以是不同的类型，包括带结构数据的复杂类型，
而层级则是指Key可以有不同的层级关系，就如目录树一样。

特性
----

### 现在

* 层级
* 结构化
* 自组织(自治)
* 按需加载
* 分页搜索

### 未来

* 索引支持
* 到期机制支持
* 历史版本支持

简介(Summary)
-------------

关系型数据存储系统数据表现为一张2维有行和列的表格，每一行都是相同固定的n列。
而Key/Value数据存储系统，却总是单列的，或者换句话说，每一行都只有一列数据。
而对于结构化的Key/Value存储系统，它的每一行的列数都是不定的，也许只有一列，
也许两列，也许n列，根据Key的不同而变化不定，而对于层级来说，随着Key的层级
不同，Value和Key的关系会不断的发生转换。

具体举一个例子，可能更容易理解些：

关系型数据库的呈现如下：

用户表(user):

|登录名(PK)| 姓   |   名|email       |
|smith     |Smith | Mary|smich@so.com|
|john      |John  | Sky |john@so.com |


项目表(project):

|项目名(PK)|标题         |拥有者|
|great     |Great Project|smith |


项目成员表(member):

|项目名(PK)|成员名(PK)|角色     |
|great     |smith     |developer|


iDB 的数据呈现：

/users/(层级1)
      smith/(层级2)
           lastName(层级3)=smith
           firstName=Mary
           email=smith@so.com
/projects/(层级1)
         great/(层级2)
              title(层级3)=Great Project
              owner=/users/smith
              members/(层级3)
                     smith/(层级4)
                          roles(层级5)=developer

我们可以看到，key "users/smith/lastName"的值是单列值，而 key "users/smith" 则
是一个固定列数的多列值，而 key “users” 则是没有固定列数长度不定的n列值。
就层级关系来看， "users/smith/lastName" 是 "users/smith"的列值, 而"users/smith"
则又是 "users“ 的列值，它们的K/V关系在不断的转化...

iDB的架构体系
-------------

* iDB 云控制器Cloud Controller
* iDB 集群控制器Cluster Controller
* iDB 节点控制器Node Controller
* iDB 存储引擎Storage Engine

<pre>

                  |Web Browser(Client)|
                          ↓ 
                  |DBCloud Controller|
                   ↓               ↓
       |DBCluster Controller|   |DBCluster Controller|
          ↓            ↓
|DBNode Controller|  |DBNode Controller|
       ↓                 ↓
    | iDB |           | iDB |


DBCloud Controller
      |__DBCluster Controller(Cluster A)
      |__DBCluster Controller(Cluster B)
      |__.......
      |__DBCluster Controller(Cluster X)
          |__DBNode Controller
          |__DBNode Controller
          |__......
          |__DBNode Controller
          |__DBNode Controller

</pre>

### iDB Cloud Controller

iDB云控制器(iDBCLC) 是暴露在互联网上顶层组件。为外部世界提供RESTful API以及Web接口，
它处理客户请求，并执行高层资源规划和帐户管理。

iDB云控制器(iDBCLC) iDB云控制器(iDBCLC) iDB云控制器(iDBCLC) iDB云控制器(iDBCLC)根据
需要可以从多个集群中聚集资源.

管理数据库集群关系：

 * Master Replication 关系
 * Slave Replication 关系
 * Cache Replication(热点数据存储，当缓存没有的时候从 master 集群取)
 * 分区Partition: by IP, by Some Field(City), by hash+cluster weight
 * 同一数据中心的集群.(distance)

注册管理集群

管理数据库：
  * Database Name
  * DB Cluster: Partition Master
  * DB Cluster: Slave
  * DB Cluster: Partition Master

### iDB 集群控制器

* 管理节点
* 数据定位器Hash (在创建时候可以选择数据分散算法: 一致性hasing 或者其他)
* 数据重定向Redirection: Only provide a Node IP for a key to redirect.

### iDB 节点控制器

* 控制数据库
* iDB 存储引擎代理(多数据存储引擎支持)

### iDB Storage Engine

iDB自己的数据存储引擎.


iDB 的数据和类型
----------------

iDB 数据库的数据项是由Key和Value组成，通过Key可以得到唯一对应的Value。
道家有云，道生一，一生二，二生三，三生万物：

    一个数据项由一个Key和一个Value组成（二），然后随着key和value出现了
    层级和结构（三）。

* 数据项         (1)
  * Key + Value  (2）
  *  |      |
  * 层级+ 结构   (3）


如此就可以构成一个非常复杂的数据存储体系。只要你愿意，甚至可以比关系型
数据库还要复杂。简单和复杂全凭一念之间。

以iDB构造关系库举例来说：

* Key: Table_Name/Item_PK
* Value: Fields List

### Key

Key 是获取Value的唯一入口项，每一个Key都唯一对应一个Value。
Key 可以是有层级的，类似于目录的层级结构。

### Value

值类型可以分为：简单类型和复杂类型。简单类型总是单一值类型。
而复杂类型则是简单类型的复合而成的类型。

### 简单值类型

* String
* Integer
  * Hex
* Boolean
* Float
* Blob

### 复杂值类型

* Dict
  * Object
  * List
  * Table
