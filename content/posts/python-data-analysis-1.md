---
title: "用python做数据分析与科学计算(篇一)"
date: 2018-03-18
categories: ["数据分析"]
tags: ["数据分析", "Python", "Machine-Learning"]
url: "/用python做数据分析与科学计算(篇一).html"
math: true
---

用python做数据分析与科学计算主要涉及Numpy, Pandas, Scipy, Scikit-learn, Scipy等库，工作环境为Anaconda，这个IDE集成了大部分常用的包。同时，可以实现本地环境下Python的多版本切换，可参考之前文章,[MacOS下使用python的多版本方案](https://ulsonhu.github.io/MacOS%E4%B8%8B%E4%BD%BF%E7%94%A8python%E7%9A%84%E5%A4%9A%E7%89%88%E6%9C%AC%E6%96%B9%E6%A1%88.html)

  通常做数据分析&挖掘的workflow：拿到数据之后先要做一个数据的预处理(pandas+numpy+scipy)，接着会要对数据包含的特征做一些可视化输出(matplotlib)，之后需要提取特征&建模调参(numpy+scikit-learn)，有了模型与结果，最后归纳整理做presentation & report.

## Numpy

用来存储和处理大型矩阵，比Python自身的嵌套列表（nested list structure)结构要高效的多，本身是由C语言开发。这个是很基础的扩展，其余的扩展都是以此为基础。数据结构为ndarray,一般有三种方式来创建。

| Function | Useage |
| --- | --- |
| array.shape | 查看或改变数组的大小 |
| array.reshape | 修改数组的尺寸，原数组不变，两个数组共享内存，如果修改值的话这两个数组都会变 |
| array.size | 数组元素的总个数，等于shape属性中元组元素的乘积 |
| array.ndim | 数组的维数 |
| array.dtype | array的数据规格 |
| numpy.zeros(dim1,dim2) | 创建dim1*dim2的零矩阵 |
| numpy.eye(n) | 创建$n*n$单位矩阵 |
| numpy.identity(n) | 创建$n*n$单位矩阵 |
| numpy.arange | 类似于list的range函数，通过指定初始值，终值，和步长来生成一维数组 |
| array.astype(numpy.float64) | 更换矩阵的数据形式 |
| array * array | 矩阵点乘 |
| array[a:b] | 切片 |
| array.copy() | 得到ndarray的副本，而不是视图 |
| array [a] [b]=array [ a, b ] | 两者等价 |
| data[[4,3,0,6]] | 索引，将第4,3,0,6行摘取出来，组成新数组 |
| numpy.reshape(a,b) | 将a*b的一维数组排列为a*b的形式 |
| array([a,b,c,d],[d,e,f,g]) | 返回一维数组，分别为[a,d],[b,e],[c,f],[d,g] |
| array.T | array的转置 |
| numpy.random.randn(a,b) | 生成$a*b$的随机数组 |
| numpy.dot(matrix_1,matrix_2) | 矩阵乘法 |
| array.transpose( (1,0,2,etc.) ) | 对于高维数组，转置需要一个由轴编号组成的元组 |

numpy库提供了matrix类，使用matrix类创建的是矩阵对象，它们的加减乘除运算缺省采用矩阵方式计算。但是由于NumPy中同时存在ndarray和matrix对象，因此很容易将两者弄混。

```python
# 利用ones()创建一个2*4的全1矩阵
>>> np.mat(np.ones((2,4))) 
matrix([[ 1.,  1.,  1.,  1.],
        [ 1.,  1.,  1.,  1.]])
```

## Pandas

基于NumPy 的一种工具，该工具是为了解决数据分析任务而创建的。Pandas 纳入了大量库和一些标准的数据模型，提供了高效地操作大型数据集所需的工具。最具有统计意味的工具包，某些方面优于R软件。数据结构有一维的Series，二维的DataFrame(类似于Excel或者SQL中的表，如果深入学习，会发现Pandas和SQL相似的地方很多，例如merge函数)，三维的Panel（Pan（el) + da(ta) + s，知道名字的由来了吧）。

学习Pandas你要掌握的是：

1. 汇总和计算描述统计，处理缺失数据 ，层次化索引
2. 清理、转换、合并、重塑、GroupBy技术
3. 日期和时间数据类型及工具

[入门理解：](http://pandas.pydata.org/pandas-docs/stable/10min.htmlml)

### 使用pandas清洗数据

```python
import pandas as pd
column_names = ["sex", "length", "diameter", "height", "whole weight", "shucked weight", "viscera weight", "shell weight", "rings"]
alone_df = pd.read_csv('alone.csv',names=column_names)
alone_df['sex'] = alone_df['sex'].map({'F':1,'M':0,'I':2})
alone_df['sex'] = alone_df.rings.map(lambda x: 1 if x > 9 else 0)
alone_df.head()
```

## Matplotlib

Python中最著名的绘图系统，很多其他的绘图例如Seaborn（针对pandas绘图而来）也是由其封装而成。其中针对不是很复杂的数据，推荐使用Seaborn，容易上手，图表美观。[Seaborn参考](http://seaborn.pydata.org/index.html)

需要掌握的内容

1. 散点图，折线图，条形图，直方图，饼状图，箱形图的绘制。
2. 绘图的三大系统：pyplot，pylab(不推荐)，面向对象
3. 坐标轴的调整，添加文字注释，区域填充，及特殊图形patches的使用
4. 金融的同学要注意的是：可以直接调用Yahoo财经数据绘图（很好用）

### 简单的散点图

```python
x = np.linspace(0, 2 * np.pi, 50)
y = np.sin(x)
plt.scatter(x,y)
plt.show()
```

![](https://res.cloudinary.com/ulsonhu/image/upload/v1521902375/2018_03_09_03.png)

### 使用子图

```python
x = np.linspace(0, 2 * np.pi, 50)
plt.subplot(2, 1, 1) # （行，列，活跃区）
plt.plot(x, np.sin(x), 'r')
plt.subplot(2, 1, 2)
plt.plot(x, np.cos(x), 'g')
plt.show()
```

![](https://res.cloudinary.com/ulsonhu/image/upload/v1521902375/2018_03_09_02.png)

使用子图只需要一个额外的步骤。即在调用 `plot()` 函数之前需要先调用`subplot()`函数。该函数的第一个参数代表子图的总行数，第二个参数代表子图的总列数，第三个参数代表活跃区域.

标题，标签和图例当需要快速创建图形时，你可能不需要为图形添加标签。但是当构建需要展示的图形时，你就需要添加标题，标签和图例。

### 添加标题，坐标轴标记和图例

```python
x = np.linspace(0, 2 * np.pi, 50)
plt.plot(x, np.sin(x), 'r-x', label='Sin(x)')
plt.plot(x, np.cos(x), 'g-^', label='Cos(x)')
plt.legend() # 展示图例
plt.xlabel('Rads') # 给 x 轴添加标签
plt.ylabel('Amplitude') # 给 y 轴添加标签
plt.title('Sin and Cos Waves') # 添加图形标题
plt.show()
```

为了给图形添加图例，我们需要在 `plot()` 函数中添加命名参数 `label` 并赋予该参数相应的标签。然后调用 `legend()` 函数就会在我们的图形中添加图例。

接下来我们只需要调用函数 `title()`，`xlabel()` 和 `ylabel()` 就可以为图形添加标题和标签。

你会得到类似于下面这张拥有标题、标签和图例的图形：

![](https://res.cloudinary.com/ulsonhu/image/upload/v1521902376/2018_03_09_04.png)

参考文献

1. [Deep Learning Tutorials](http://deeplearning.net/tutorial/)
2. [Scipy Lecture](http://www.scipy-lectures.org/)
3. [KeSci平台](https://www.kesci.com/)
4. [10 Minutes to pandas](http://pandas.pydata.org/pandas-docs/stable/10min.html)
