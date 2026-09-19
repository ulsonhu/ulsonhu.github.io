---
title: "SAS基础学习篇(一)"
date: 2018-03-14
categories: ["数据分析"]
tags: ["数据分析", "SAS"]
description: "由于接触到SAS，本人电脑为Macbook，暂时无法安装SAS，所以通过网上收集相关知识，Mark下"
url: "/SAS基础学习篇(一).html"
math: true
---

参考书籍

1. 《SAS编程与数据挖掘商业案例》（预热）
2. 「the Little SAS Book」(推荐)
3. 「Applied Econometrics Using The SAS System」

SAS编程主要包括`DATA`和`PROC`两部分

```plain
* create sas data set named toads;
* read the data file ToadJump.dta using list input;
DATA toads;
INFILE '~/desktop/ToadJump.dta';
INPUT ToadJump $ Weight Jump1 Jump2 Jump3;
RUN;
* print the data to make sure the file was read correctly;
* PROC PRINT DATA = toads;
TITLE 'SAS Data Set Toads';
RUN;
```

这样就建立了一个名为`toads`的临时数据集，然后读入外部文件`ToadJump.dat`，然后告诉SAS有四个变量，其中第一个是文本型,缺失值用一个点`.`标记

```plain
* Create a SAS data set named sales;
* Read the data file OnionRing.dat using column input;
DATA sales;
INFILE ’~/desktop/OnionRing.dat’;
INPUT VisitingTeam $ 1-20 ConcessionSales 21-24 BleacherSales 25-28
OurHits 29-31 TheirHits 32-34 OurRuns 35-37 TheirRuns 38-40;
RUN;
* Print the data to make sure the file was read correctly;
PROC PRINT DATA = sales;
TITLE ’SAS Data Set Sales’;
RUN;
```

## 基本函数

| SAS文本类函数 |  |
| --- | --- |
| ANYALNUM(arg,start) | 返回第一次出现任意数字或字母的位置，可选开始位置start |
| ANYALPHA(arg,start) | 返回第一次出现任意字母的位置，可选开始位置start |
| ANYDIGIT(arg,start) | 返回第一次出现任意数字的位置，可选开始位置start |
| ANYSPACE(arg,start) | 返回第一次出现任意空白的位置，可选开始位置start |
| CAT(arg1,arg2,…argn) | 连接字符串，留下头尾空白 |
| CATS(arg1,arg2,…argn) | 连接字符串，删除头尾空白 |
| CATX(‘separator-string’, arg-1,…,arg-n) | 连接字符串，删除头尾空白并用指定标点连接 |
| COMPRESS(arg, ‘char’) | 移除字符串中的空格和可选字符 |
| INDEX(arg, ‘string’) | 返回指定字符在变量中的位置 |
| LEFT(arg) | 字符串左对齐 |
| LENGTH(arg) | 返回字符串长度，不考虑尾部空格 |
| PROPCASE(arg) | 首字母大写 |
| SUBSTR(arg,position,n) | 从字符串中提取指定开始位置指定长度字符 |
| TRANSLATE(source,to1,from1,…ton,fromn) | 替换字符 |
| TRANWRD(source,from,to) | 替换字符串 |
| TRIM(arg) | 删除尾部空白 |
| UPCASE(arg) | 替换成大写 |

| SAS数值函数 |  |
| --- | --- |
| INT(arg) | 返回整数 |
| LOG(arg) | 自然对数 |
| LOG10(arg) | $10$为底对数 |
| MAX(arg1,arg2,…argn) | 最大值 |
| MEAN(arg1,arg2,…argn) | 均值 |
| MIN(arg1,arg2,…argn) | 最小值 |
| N(arg1,arg2,…argn) | 非缺失值个数 |
| NMISS(arg1,arg2,…argn) | 缺失值个数 |
| ROUND(arg, roundoffunit) | 保留几位小数 |
| SUM(arg1,arg2,…argn) | 求和 |

| SAS日期函数 |  |
| --- | --- |
| DATEJUL(julian-date) | 标准julian日期到SAS日期 |
| DAY(date) | 返回「日」 |
| MDY(month,day,year) | 年月日到SAS日期 |
| MONTH(date) | 返回「月」 |
| QTR(date) | 返回季度 |
| TODAY() | 今日 |
| WEEKDAY(date) | 返回周几（周日为1） |
| YEAR(date) | 返回「年」 |
| YRDIF(start-date,end- date,’ACTUAL’) | 返回相差年份 |

## 判断结构

```plain
* if then structure
if model = 'Pink' then make = 'Floyd';

* 执行多项命令，需要嵌套do；可以用and和or
if Year then Model = 'Mac' or Model = 'pro' then Make = 'Jobs';
if Model = 'iphone5' then do;
Make = 'Tim';
Seats = 2;
end;

* if else
if Cost = . then CostGroup = 'Missing';
else if Cost else if Cost else CostGroup = high;

* use if to select sub-set
if sex = 'm';if sex = 'm' then detele;
```

## 数组操作

```plain
* Change all 9 to missing values;
DATA songs;
INFILE '~/desktop/WBRK.dat';
INPUT City $ 1-15 Age domk wj hwow simbh kt aomm libm tr filp ttr;
ARRAY song (10) domk wj hwow simbh kt aomm libm tr filp ttr;
DO i = 1 TO 10;
IF song(i) = 9 THEN song(i) = .;
END;
RUN;
PROC PRINT DATA = songs;
TITLE 'WBRK Song Survey';
RUN;
```

## 基本模块调用

搞定基本的函数之后，开始鼓捣$SAS$里面的模型。也就是说，要开始写`PROC`了。其实，$SAS$比较像$Stata$（计量经济学主流软件），无论是从输出的样式，还是语法。不习惯没有()的模型调用呀。若是说$SAS$和$Stata$的区别，怕只是$Stata$更侧重于**计量模型**而$SAS$则是服务于大多数**统计模型**吧。

### PROC的基本内容：CONTENT

`PROC:content`，可以显示数据集的主要特性。比如，

```plain
LIBNAME tropical '~/MySASLib';
PROC CONTENTS DATA = tropical.banana;
```

这里主要是两个声明:`TITLE`和`FOOTNOTE`。前者输出时候会产生一个标题，后者会产生尾注。用法也是比较直接的：

```plain
TITLE ”Here’s another title”;
TITLE ’Here’’s another title’;
FOOTNOTE3 ’This is the third footnote’;
```

### SAS PROC求子集:WHERE

如果要在`PROC`里面先求子集的话，可以直接调用`WHERE`。感觉这里和$SQL$的思路比较像。

```plain
PROC PRINT DATA = '～/desktop/MySASLib/style';
WHERE Genre = 'Impressionism';
TITLE 'Major Impressionist Painters';
FOOTNOTE 'F = France N = Netherlands U = US';
RUN;
```

### SAS PROC 数据进行排序:SORT

```plain
DATA marine;
INFILE '~/desktop/Lengths.dat';
INPUT Name $ Family $ Length @@;
RUN;
* Sort the data;
PROC SORT DATA = marine OUT = seasort NODUPKEY;
BY Family DESCENDING Length;
PROC PRINT DATA = seasort;
TITLE 'Whales and Sharks';
RUN;
```

这样数据就按照`Family`、`Length`（递减）排序了。

### SAS PROC 输出数据:PRINT

```plain
DATA sales;
INFILE '~/desktop/Candy.dat';
INPUT Name $ 1-11 Class @15 DateReturned MMDDYY10. CandyType $
Quantity;
Profit = Quantity * 1.25;
PROC SORT DATA = sales;
BY Class;
PROC PRINT DATA = sales;
BY Class;
SUM Profit;
VAR Name DateReturned CandyType Profit;
TITLE 'Candy Sales for Field Trip by Class';
RUN;
```

### SAS PROC里面改变输出格式：FORMAT

基本就是`FORMAT`一下就可以了，再就是`PUT`的时候也可以调整。

```plain
DATA sales;
INFILE '~/desktop/Candy.dat';
INPUT Name $ 1-11 Class @15 DateReturned MMDDYY10. CandyType $
Quantity;
Profit = Quantity * 1.25;
PROC PRINT DATA = sales;
VAR Name DateReturned CandyType Profit;
FORMAT DateReturned DATE9. Profit DOLLAR6.2;
TITLE 'Candy Sale Data Using Formats';
RUN;
```

常用的格式有：

- 文本型：`$HEXw.`和`$w.`
- 日期型：`DATEw.`（输出为ddmmyy或者ddmmyyyy）、`DATETIMEw.d`（输出为ddmmyy:hh:mm:ss）、`DAYw.`（输出为dd）、`EURDFDDw.` 、`JULIANw.`、`MMDDYYw.`（输出为mmddyy或mmddyyyy）、`TIMEw.d`（输出为hh:mm:ss）、`WEEKDATEw.`（输出为工作日）、`WORDDATEw.`(输出为单词)。
- 数字型：`BESTw.`（自动选择）、`COMMAw.d`（逗号分隔）、`DOLLARw.d`（货币）、`Ew.`（科学计数法）、`PDw.d`、`w.d`（标准小数）

输出的样本见下：

当然`FORMAT`还可以自定义`factor`型变量的输出格式，比如：

```plain
DATA carsurvey;
INFILE '~/deskktop/Cars.dat';
INPUT Age Sex Income Color $;
PROC FORMAT;
VALUE gender 1 = 'Male' 
2 = 'Female';
VALUE agegroup 13 -< 20 = 'Teen'
20 -< 65 = 'Adult'
65 - HIGH = 'Senior';
VALUE $col 'W' = 'Moon White'
'B' = 'Sky Blue'
'Y' = 'Sunburst Yellow'
'G' = 'Rain Cloud Gray';
* Print data using user-defined and standard (DOLLAR8.) formats;
PROC PRINT DATA = carsurvey;
FORMAT Sex gender. Age agegroup. Color $col. Income DOLLAR8.;
TITLE 'Survey Results Printed with User-Defined Formats';
RUN;
```

就可以把数字型的1，2转换为对应的文本`male`和`female`等，还可以把变量离散化。

### SAS总结数据:MEANS

$SAS$当然还有类似于$Excel$的数据透视表和$R$的`data.table`的模块，就是`MEANS`。可以输出的描述性统计值，包括最大值、最小值、平均值、中位数、余非缺失值个数、缺失值个数、范围、标准差、和等等。此外，还可以使用`BY`或者`CLASS`进行分组统计，`VAR`选择变量等。

```plain
DATA sales;
INFILE '~/desktop/Flowers.dat';
INPUT CustomerID $ @9 SaleDate MMDDYY10. Petunia SnapDragon
Marigold;
Month = MONTH(SaleDate);
PROC SORT DATA = sales;
BY Month;
* Calculate means by Month for flower sales;
PROC MEANS DATA = sales;
BY Month;
VAR Petunia SnapDragon Marigold;
TITLE 'Summary of Flower Sales by Month';
RUN;
```

可以实现

```plain
 Summary of  Flower Sales by Month 1
---------------- Month=5 --------------
The MEANS Procedure
Variable N Mean Std Dev Minimum Maximum
----------------------------------------
Petunia 3 86.6666667 35.1188458 50.0000000 120.0000000
SnapDragon 3 113.3333333 41.6333200 80.0000000 160.0000000
Marigold 3 81.6666667 25.6580072 60.0000000 110.0000000
---------------- Month=6 ---------------
Variable N Mean Std Dev Minimum Maximum
-----------------------------------------
Petunia 4 81.2500000 16.5201897 60.0000000 100.0000000
SnapDragon 4 97.5000000 47.8713554 60.0000000 160.0000000
Marigold 4 83.7500000 19.7378655 60.0000000 100.0000000
-------------------------------------------
```

当然这些统计量也可以直接的写入一个SAS数据表，只需要加上一个`OUTPUT`就可以了。原数据：

```plain
756-01 05/04/2008 120 80 110
834-01 05/12/2008 90 160 60
901-02 05/18/2008 50 100 75
834-01 06/01/2008 80 60 100
756-01 06/11/2008 100 160 75
901-02 06/19/2008 60 60 60
756-01 06/25/2008 85 110 100
```

SAS代码：

```plain
DATA sales;
INFILE '~/desktop/Flowers.dat';
INPUT CustomerID $ @9 SaleDate MMDDYY10. Petunia SnapDragon Marigold;
PROC SORT DATA = sales;
BY CustomerID;
* Calculate means by CustomerID, output sum and mean to new data set;
PROC MEANS NOPRINT DATA = sales;
BY CustomerID;
VAR Petunia SnapDragon Marigold;
OUTPUT OUT = totals MEAN(Petunia SnapDragon Marigold) =
MeanPetunia MeanSnapDragon MeanMarigold
SUM(Petunia SnapDragon Marigold) = Petunia SnapDragon Marigold;
PROC PRINT DATA = totals;
TITLE 'Sum of Flower Data over Customer ID';
FORMAT MeanPetunia MeanSnapDragon MeanMarigold 3.;
RUN;
```

最终结果为：![](https://res.cloudinary.com/ulsonhu/image/upload/v1521555460/2018_03_07_01.png)

### SAS PROC统计频率：FREQ

计数的话，就要靠SAS里面的`FREQ`模块了。比如我们有一个数据集：

```plain
esp w cap d cap w kon w ice w kon d esp d kon w ice d esp d
cap w esp d cap d Kon d . d kon w esp d cap w ice w kon w
kon w kon w ice d esp d kon w esp d esp w kon w cap w kon w
```

然后可以用`FREQ`来统计一些基本量：

```plain
DATA orders;
INFILE '~/desktop/Coffee.dat';
INPUT Coffee $ Window $ @@;
* Print tables for Window and Window by Coffee;
PROC FREQ DATA = orders;
TABLES Window Window * Coffee;
RUN;
```

最终会得到一个$2*5$的表格：![](https://res.cloudinary.com/ulsonhu/image/upload/v1521555460/2018_03_07_02.png)

### SAS PROC汇报表格：TABULATE

基本看到TABULATE就可以想到那个著名的软件Tabular了…不过貌似SAS也自带了一个类似的表格模块。这个东西可以变得非常复杂，不过鉴于一时半会儿还用不到，没有细细看。抄个例子吧。

原数据：

```plain
Silent Lady Maalea sail sch 75.00
America II Maalea sail yac 32.95
Aloha Anai Lahaina sail cat 62.00
Ocean Spirit Maalea power cat 22.00
Anuenue Maalea sail sch 47.50
Hana Lei Maalea power cat 28.99
Leilani Maalea power yac 19.99
Kalakaua Maalea power cat 29.50
Reef Runner Lahaina power yac 29.95
Blue Dolphin Maalea sail cat 42.95
```

SAS代码：

```plain
DATA boats;
INFILE '~/desktop/Boats.dat';
INPUT Name $ 1-12 Port $ 14-20 Locomotion $ 22-26 Type $ 28-30
Price 32-36;
RUN;
* Tabulations with three dimensions;
PROC TABULATE DATA = boats;
CLASS Port Locomotion Type;
TABLE Port, Locomotion, Type;
TITLE 'Number of Boats by Port, Locomotion, and Type';
RUN;
```

最终结果：![](https://res.cloudinary.com/ulsonhu/image/upload/v1521555460/2018_03_07_03.png)

类似的，还可以增加统计量（类似于`MEANS`那里）：

```plain
DATA boats;
INFILE '~/desktop/Boats.dat';
INPUT Name $ 1-12 Port $ 14-20 Locomotion $ 22-26 Type $ 28-30
Price 32-36;
RUN;
* PROC TABULATE report with options;
PROC TABULATE DATA = boats FORMAT=DOLLAR9.2;
CLASS Locomotion Type;
VAR Price;
TABLE Locomotion ALL, MEAN*Price*(Type ALL)
/BOX='Full Day Excursions' MISSTEXT='none';
TITLE;
RUN;
```

可以得到：![](https://res.cloudinary.com/ulsonhu/image/upload/v1521555460/2018_03_07_04.png)

最后还可以混合`FORMAT`等等，可以变得相当的复杂。貌似这东西是美国劳工部鼓捣出来的格式…

```plain
DATA boats;
INFILE '~/desktop/Boats.dat';
INPUT Name $ 1-12 Port $ 14-20 Locomotion $ 22-26 Type $ 28-30
Price 32-36 Length 38-40;
RUN;
* Using the FORMAT= option in the TABLE statement;
PROC TABULATE DATA = boats;
CLASS Locomotion Type;
VAR Price Length;
TABLE Locomotion ALL,
MEAN * (Price*FORMAT=DOLLAR6.2 Length*FORMAT=6.0) * (Type ALL);
TITLE 'Price and Length by Type of Boat';
RUN;
```

BOSS级汇报表格呈现了…

![](https://res.cloudinary.com/ulsonhu/image/upload/v1521555460/2018_03_07_05.png)

我只能感慨，不愧是商业软件啊，用户需求考虑的真的是特别的周到…这种费时费力做汇报表格的事情也被搞定了，强悍。

SAS里面的报告：REPORT还有一个REPORT，看到有TABULATE的时候我已经不奇怪并略略的有些期待一个做报告的模块出现了。这东西基本就是前面几个的超级混合体，反正你想搞到的汇报模式总是能够搞出来的。

又是一堆数据：

```plain
17 sci 9 bio 28 fic 50 mys 13 fic 32 fic 67 fic 81 non 38 non
53 non 16 sci 15 bio 61 fic 52 ref 22 mys 76 bio 37 fic 86 fic
49 mys 78 non 45 sci 64 bio 8 fic 11 non 41 fic 46 ref 69 fic
34 fic 26 mys 23 sci 74 ref 15 sci 27 fic 23 mys 63 fic 78 non
40 bio 12 fic 29 fic 54 mys 67 fic 60 fic 38 sci 42 fic 80 fic
```

然后一堆SAS代码：

```plain
DATA books;
INFILE 'c:\MyRawData\LibraryBooks.dat';
INPUT Age BookType $ @@;
RUN;
* Define formats to group the data;
PROC FORMAT;
VALUE agegpa
0-18 = '0 to 18'
19-25 = '19 to 25'
26-49 = '26 to 49'
50-HIGH = ' 50+ ';
VALUE agegpb
0-25 = '0 to 25'
26-HIGH = ' 26+ ';
VALUE $typ
'bio','non','ref' = 'Non-Fiction'
'fic','mys','sci' = 'Fiction';
RUN;
*Create two way table with Age grouped into four categories;
PROC FREQ DATA = books;
TITLE 'Patron Age by Book Type: Four Age Groups';
TABLES BookType * Age / NOPERCENT NOROW NOCOL;
FORMAT Age agegpa. BookType $typ.;
RUN;
* Create two way table with Age grouped into two categories;
PROC FREQ DATA = books;
TITLE 'Patron Age by Book Type: Two Age Groups';
TABLES BookType * Age / NOPERCENT NOROW NOCOL;
FORMAT Age agegpb. BookType $typ.;
RUN;
```

然后一堆交叉计数的结果就出来了：![](https://res.cloudinary.com/ulsonhu/image/upload/v1521555460/2018_03_07_06.png)

当然，简单的计算和分类统计也不在话下：

```plain
DATA natparks;
INFILE 'c:\MyRawData\Parks.dat';
INPUT Name $ 1-21 Type $ Region $ Museums Camping;
RUN;
*Statistics in COLUMN statement with two group variables;
PROC REPORT DATA = natparks NOWINDOWS HEADLINE;
COLUMN Region Type N (Museums Camping),MEAN;
DEFINE Region / GROUP;
DEFINE Type / GROUP;
TITLE 'Statistics with Two Group Variables';
RUN;
*Statistics in COLUMN statement with group and across variables;
PROC REPORT DATA = natparks NOWINDOWS HEADLINE;
COLUMN Region N Type,(Museums Camping),MEAN;
DEFINE Region / GROUP;
DEFINE Type / ACROSS;
TITLE 'Statistics with a Group and Across Variable';
RUN;
```

可以得到一个看起来很fancy的表格：![](https://res.cloudinary.com/ulsonhu/image/upload/v1521555460/2018_03_07_07.png)

### SAS数据总结综述

我的感觉是，`MEANS`, `TABULATE`和`REPORT`这三个模块各有千秋，基本就是可以替代EXCEL的数据透视表，虽然效率上说不好谁比谁高。
