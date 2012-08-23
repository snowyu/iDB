# Protocol

## Messages



### String

    (len)string\0

* len:
  * len < 128($80): size(len)=1byte(8bit)
  * 128($80) >= len <= $7FFF: size(len)=2byte(16bit)
  * len >= $8000: size(len)=4byte(32bit)
* string
* last char(byte): Special Defined Char
  * \0: NULL String Terminator.
  * \1: Not Loaded Complex ValueType. eg, (0)\1, len=0

### Dict

* index by key

    {key:v, key:v, ...}
    (count)KStringVTypeStringVString...

* count=16bit unsigned word

### List

* index by integer

    [v,v,v,...]
    (count)VTypeStringVString...

* count=16bit unsigned word

