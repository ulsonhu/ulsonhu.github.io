---
title: "Excel知识点备忘"
date: 2018-03-12
categories: ["数据分析"]
tags: ["Excel", "数据分析"]
description: "数据分析需要掌握的一些基本Excel姿势拾遗，后续不断更新"
url: "/Excel知识点备忘.html"
math: true
---

Excel系统学习：[视频教程](http://study.163.com/course/courseMain.htm?courseId=670032)

## 相对引用与绝对引用

- `$A1`列绝对引用
- `A$1`行绝对引用
- `$A$1`行列都为绝对引用

快捷键`F4`

## 条件格式

学会使用条件格式，其中与混合应用交叉，可实现相关功能

## 排序

- 一般排序
- 多条件排序
- 按照特定字段排序
- 排序的延伸

## 筛选

## 一、时间与日期函数

1. `today()`返回日期格式的当前日期,输入日期快捷键`Ctrl+;`
2. `now()`,输入日期时间快捷键`Ctrl+Shift+;`
3. `weekday(serial_number,return_type)`
4. `workday()`
5. `dateif(start_date,end_date,unit[Y|M|D])`返回两个日期之间年/月/日的间隔数

输入日期快捷键`Ctrl+;`

## 二、统计函数

1. `count`
2. `countif(range,criteria)`计算区域中满足指定条件的单元格个数
3. `countifs(range1,criteria1,range2,criteria2,...)`
4. `sumif(range,criteria,sum_range)`
5. `sumifs(sum_range,criteria_range1,criteria1,criteria_range2,criteria2,...)`

## 三、查找和引用函数

1. `vlookup(lookup_value,table_array,col_index_num,range_lookup)`

- `lookup_value`需要在数据表第一列查找的数值
- `table_array`需要查找的数据区域
- `col_index_num`为待返回的匹配值的列序号
- `range_lookup`精确匹配与模糊匹配

### 关于跨表引用

| 产品编号 | 系列 | 产品名称 | 进货单价 |
| --- | --- | --- | --- |
| AP11001 | 老婆饼 | 老婆饼（花生） | 6.5 |
| AP11002 | 老婆饼 | 老婆饼（桂花） | 6.5 |

如根据“产品编号”自动返回基本信息表“系列”字段内容`vlookup($D2,产品基本信息表!$B$3:$F$38,2,false)`

> 跨表查询，工作中常用

注意：

- 查找值一定要在第一列
- 模糊匹配时第一列一定要升序排列

2. `index(查找的区域，区域内第几行，区域内第几列)`与`match(查找指定的值，查找所在区域，查找方式的参数)`，两者连用，基本可以替代’Vlookup()'的查找，其中’Vlookup()'只是针对文本内容的查找

如`index(A:A,match(C1,B:B,0))`

3. > =Lookup（查找的值，值所在的位置，返回相应位置的值）

`lookup()`函数弥补了`vlookup()`函数第三参数的劣势，但其本身也存在缺点，即不能精确匹配使用`lookup()`函数需要熟悉Excel数组的运算.详见[视频18课时62:00](http://study.163.com/course/courseLearn.htm?courseId=670032#/learn/video?lessonId=823422&courseId=670032)

4. `choose(index_num, value1, [value2], ...)`
5. `Offset(指定点，偏移多少行，偏移多少列，返回多少行，返回多少列)`建立坐标系，以坐标系为原点，返回距离原点的值或者区域。正数代表向下或向右，负数则相反。通过’Offset()'函数可以实现动态图标、动态数据透视表
6. `Row()`

返回单元格所在的行

7. `Column()`

返回单元格所在的列

## 四、文本函数

- `text(text)`设置数字格式并将其转换为文本
- `concatenate(text1,text2,...)`将几个文本项合并为一个文本项
- `len(text)`计算字符串的长度
- `mod(number,divisor)` 返回两数相除的余数。
- `right(text,num_chars)` 返回文本值中最右边的字符
- `left(text,num_chars)`返回文本值中最左边的字符
- `mid(text,start_num,num_chars))`从文本字符串中的指定位置起返回特定个数的字符
- `trim(text)`设置数字格式并将其转换为文本

## 五、数据透视表

Excel中十分重要的一项功能，主要功能是将数据聚合，按照各子段进行`sum()`，`count()`的运算。应用范围

- 包括大量复杂数据的表格，希望快速整理出一份具有实际意义的报表
- 希望找出同类数据在不同时期的某种特定关系
- 希望对数据进行合理有效的分组
- 需要经常查询分析数据的变化趋势
- 数据源经常变化，然而有需要经常分析和处理最新的数据源

### 数据分析

查找`Ctrl+F`与替换

```plain
=if(average(A2:A5)>50,sum(B2:B5),0)
=if(A2=10,"科技处",if(A2=20,"财务处","人事处"))
=sumif(销售记录汇总!$A$2:$A$107,$B5,销售记录汇总!$G$2,$G$107)
=sumif(条件区域,条件值,求和区域)

=sumifs(求和区域,条件区域,条件值)
=sumif(销售记录汇总!$G$2,$G$107,销售记录汇总!$A$2:$A$107,$B5)
```

条件可以是数字、表达式或文本，但是要使用引号

### 数组计算相关

计算结果`Ctrl+Shift+Enter`

## 杂类技巧

1. 选择性粘贴 $\rightarrow $ 转置
2. ``` column()``row() ```返回当前列(行)数
3. `Ctrl+Enter`，以当前单元格为始，往下填充数据和函数。
4. `Ctrl+Space`，选定整列。`Shift+Space`，选定整行。
5. `Alt+Enter`，换行。
