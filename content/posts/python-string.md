---
title: "Python字符串处理拾掇"
date: 2017-04-20
categories: ["机器学习相关"]
tags: ["Python"]
description: "python中有些常用的字符串处理函数,特别是用python处理自然语言时，字符串处理用的十分频繁。下面总结一下常用的字符串处理的相关函数："
url: "/Python字符串处理拾掇.html"
---

Python 字符串操作（string替换、删除、截取、复制、连接、比较、查找、包含、大小写转换）

一、去空格及特殊符号

```python
s.strip().lstrip().rstrip(',')
```

二、复制字符串

```python
# strcpy(sStr1,sStr2)
sStr1 = 'strcpy'
sStr2 = sStr1
sStr1 = 'strcpy2'
print(sStr2)
```

三、连接字符串

```python
#strcat(sStr1,sStr2)
sStr1 = 'strcat'
sStr2 = 'append'
sStr1 += sStr2
print(sStr1)
```

四、查找字符

```python
#strchr(sStr1,sStr2)
# < 0 为未找到
sStr1 = 'strchr'
sStr2 = 's'
nPos = sStr1.index(sStr2)
print(nPos)
```

五、比较字符串

```python
#strcmp(sStr1,sStr2)
sStr1 = 'strchr'
sStr2 = 'strch'
print(cmp(sStr1,sStr2))
```

六、扫描字符串是否包含指定的字符

```python
#strspn(sStr1,sStr2)
sStr1 = '12345678'
sStr2 = '456'
#sStr1 and chars both in sStr1 and sStr2
print(len(sStr1 and sStr2))
```

七、字符串长度

```python
#strlen(sStr1)
sStr1 = 'strlen'
print(len(sStr1))
```

八、将字符串中的大小写转换

```python
#strlwr(sStr1)
sStr1 = 'JCstrlwr'
sStr1 = sStr1.upper()
#sStr1 = sStr1.lower()
print(sStr1)
```

九、追加指定长度的字符串

```python
#strncat(sStr1,sStr2,n)
sStr1 = '12345'
sStr2 = 'abcdef'
n = 3
sStr1 += sStr2[0:n]
print(sStr1)
```

十、字符串指定长度比较

```python
#strncmp(sStr1,sStr2,n)
sStr1 = '12345'
sStr2 = '123bc'
n = 3
print( cmp(sStr1[0:n],sStr2[0:n]))
```

十一、复制指定长度的字符

```python
#strncpy(sStr1,sStr2,n)
sStr1 = ''
sStr2 = '12345'
n = 3
sStr1 = sStr2[0:n]
print(sStr1)
```

十二、将字符串前n个字符替换为指定的字符

```python
#strnset(sStr1,ch,n)
sStr1 = '12345'
ch = 'r'
n = 3
sStr1 = n * ch + sStr1[3:]
print(sStr1)
```

十三、扫描字符串

```python
#strpbrk(sStr1,sStr2)
sStr1 = 'cekjgdklab'
sStr2 = 'gka'
nPos = -1
for c in sStr1:
    if c in sStr2:
        nPos = sStr1.index(c)
        break
print( nPos)
```

十四、翻转字符串

```python
#strrev(sStr1)
sStr1 = 'abcdefg'
sStr1 = sStr1[::-1]
print(sStr1)
```

十五、查找字符串

```python
#strstr(sStr1,sStr2)
sStr1 = 'abcdefg'
sStr2 = 'cde'
print(sStr1.find(sStr2))
```

十六、分割字符串

```python
#strtok(sStr1,sStr2)
sStr1 = 'ab,cde,fgh,ijk'
sStr2 = ','
sStr1 = sStr1[sStr1.find(sStr2) + 1:]
print(sStr1)
#或者
s = 'ab,cde,fgh,ijk'
print(s.split(','))
```

十七、连接字符串

```python
delimiter = ','
mylist = ['Brazil', 'Russia', 'India', 'China']
print(delimiter.join(mylist))
PHP 中 addslashes 的实现
def addslashes(s):
    d = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
    return ''.join(d.get(c, c) for c in s) 
s = "John 'Johny' Doe (a.k.a. \"Super Joe\")\\\0"
print(s)
print( addslashes(s))
```

十八、只显示字母与数字

```python
def OnlyCharNum(s,oth=''):
    s2 = s.lower();
    fomart = 'abcdefghijklmnopqrstuvwxyz0123456789'
    for c in s2:
        if not c in fomart:
            s = s.replace(c,'');
    return s;
 
print(OnlyStr("a000 aa-b"))
```

十九、截取字符串

```python
str = ’0123456789′
print str[0:3] #截取第一位到第三位的字符
print str[:] #截取字符串的全部字符
print str[6:] #截取第七个字符到结尾
print str[:-3] #截取从头开始到倒数第三个字符之前
print str[2] #截取第三个字符
print str[-1] #截取倒数第一个字符
print str[::-1] #创造一个与原字符串顺序相反的字符串
print str[-3:-1] #截取倒数第三位与倒数第一位之前的字符
print str[-3:] #截取倒数第三位到结尾
print str[:-5:-3] #逆序截取，具体啥意思没搞明白？
```

二十、直接贴过来

```python
str = "Hello My friend"
# 字符串是一个整体。如果你想直接修改字符串的某一部分，是不可能的。
# 但我们能够读出字符串的某一部分。
# 子字符串的提取
str[:6]
# 字符串包含判断操作符：in，not in
"He" in str
"she" not in str

# string模块，还提供了很多方法，如
S.find(substring, [start [,end]]) #可指范围查找子串，返回索引值，否则返回-1
S.rfind(substring,[start [,end]]) #反向查找
S.index(substring,[start [,end]]) #同find，只是找不到产生ValueError异常
S.rindex(substring,[start [,end]])#同上反向查找
S.count(substring,[start [,end]]) #返回找到子串的个数

S.lowercase()
S.capitalize()      #首字母大写
S.lower()           #转小写
S.upper()           #转大写
S.swapcase()        #大小写互换

S.split(str, ' ')   #将string转list，以空格切分
S.join(list, ' ')   #将list转string，以空格连接

# 处理字符串的内置函数
len(str)                #串长度
cmp("my friend", str)   #字符串比较。第一个大，返回1
max('abcxyz')           #寻找字符串中最大的字符
min('abcxyz')           #寻找字符串中最小的字符

# string的转换
            
float(str) #变成浮点数，float("1e-1")  结果为0.1
int(str)        #变成整型，  int("12")  结果为12
int(str,base)   #变成base进制整型数，int("11",2) 结果为2
long(str)       #变成长整型，
long(str,base)  #变成base进制长整型，

# 字符串的格式化（注意其转义字符，大多如C语言的，略）
str_format % (参数列表) #参数列表是以tuple的形式定义的，即不可运行中改变
>>>print ""%s's height is %dcm" % ("My brother", 180)
          #结果显示为 My brother's height is 180cm
```
