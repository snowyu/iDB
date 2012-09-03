iDB - 下一代面向列结构化层级数据库(Structed-Column Oriented Hierarchy Database)
=========================================================================

iDB 是结构化的面向列层级数据存储系统，所谓面向列(Column)是和面向行(Row)相对
而言的，绝大多数的关系型数据库就是面向行存储的，而iDB则是面向列基于Key/Value
的存储系统，所谓结构化是指值(Value)可以是不同的类型，包括带结构数据的复杂类型，
而层级则是指Key可以有不同的层级关系，就如目录树一样。


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

|登录名| 姓   |   名|email       |
|smith |Smith | Mary|smich@so.com|
|john  |John  | Sky |john@so.com |


项目表(project):

|项目名|标题         |拥有者|
|great |Great Project|smith |


成员表(member):

|项目名|成员名|角色     |
|great |smith |developer|


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


iDB 的数据和类型
-------------

Tao 生1： 数据 

Key + Value （生2）
  + 层级 （生3）

3生万物：

iDB 数据本身是由Key, Value构成，加上层级关系，就可以构成一个非常复杂的数据存储系统。
只要你愿意，甚至可以比关系型数据库还要复杂。

而值类型也是如此

简单类型，复杂类型
   组合

### 简单类型

* String
* Integer
  * Hex
* Boolean
* Float
* Blob

### 复杂类型

* Object
* Dict
* List

