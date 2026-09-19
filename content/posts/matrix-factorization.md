---
title: "矩阵分解相关知识回顾"
date: 2017-01-21
categories: ["数理统计"]
tags: ["统计学", "Mathematic"]
description: "大学线性代数课程中我们学习了很多关于矩阵分解的方法，这些在概率统计、统计机器学习等方面都有很多应用。"
url: "/矩阵分解相关知识回顾.html"
math: true
---

## 特征值与特征向量

设A是数域F上的n阶矩阵，如果存在数域F中的一个数$\lambda$与数域上F的非零向量$\overrightarrow{\alpha}$，使得：$A\overrightarrow{\alpha}=\lambda \overrightarrow{\alpha}$则称$\lambda$为A的一个特征值(根)(eigenvalue)，称$\overrightarrow{\alpha}$为A的属于特征值$\lambda$的特征向量(eigenvector)。

显然从上式可以看出，$A\overrightarrow{\alpha} \overrightarrow{\alpha}$平行。

将上式做一下变换：$A\overrightarrow{\alpha}=\lambda \overrightarrow{\alpha}$$A\overrightarrow{\alpha}-\lambda \overrightarrow{\alpha}=0$$A\overrightarrow{\alpha}-\lambda E\overrightarrow{\alpha}=0$$(A−\lambda E)\overrightarrow{\alpha}=0$$(\lambda E-A)\overrightarrow{\alpha}=0$

称：$\lambda E−A$为A的特征矩阵行列式$f(\lambda )=|\lambda E−A|$为A的特征多项式$|\lambda E−A|=0$为A的特征方程$(\lambda E−A)\overrightarrow{x}=\overrightarrow{0}$是A关于该λ的齐次线性方程组

## 矩阵对角化

设n阶方阵A存在n个线性无关的特征向量$\overrightarrow{ x_{i} }$，将这n个特征向量$\overrightarrow {x_{i} }$组成方阵S(也称为特征向量矩阵），则有：![这里写图片描述](http://img.blog.csdn.net/20170225194650882?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdG91cmlzdG1hbjU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)这个式子称为$A$的$SΛS^{−1}$分解，或特征分解(Eigendecomposition)，或A的对角化。

根据这个式子可以知道：当方阵$A$可以被分解为某个矩阵$S$乘以某个对角矩阵$\Lambda$再乘以矩阵$S^{−1}$时，就是一次特征分解。

可以对角化的前提是$A$有$n$个线性无关的特征向量。$A$有$n$个线性无关的特征向量的前提是，所有的$\lambda$都不重复（没有重根）。

## LU分解

设$A$是一个方块矩阵。A的$LU$分解是将它分解成如下形式：$A=LU$其中$L$和$U$分别是下三角矩阵和上三角矩阵。

例如对于一个 $3*3$的矩阵，就有

![null](http://img.blog.csdn.net/20170225191810280?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdG91cmlzdG1hbjU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

一个$LDU$分解是一个如下形式的分解：$A=LDU$其中$D$是对角矩阵，$L$和$U$是单位三角矩阵（对角线上全是1的三角矩阵）。

一个$LUP$分解是一个如下形式的分解：$A=LUP$其中$L$和$U$仍是三角矩阵，$P$是一个置换矩阵。

一个充分消元的$LU$分解为如下形式：$PAQ=LU$

### 存在性

一个可逆矩阵可以进行$LU$分解当且仅当它的所有子式都非零。如果要求其中的$L$矩阵（或$U$矩阵）为单位三角矩阵，那么分解是唯一的。同理可知，矩阵的$LDU$可分解条件也相同，并且总是唯一的。

## 奇异值分解

假设M是一个m×n阶矩阵，其中的元素全部属于域K，也就是实数域或复数域。如此则存在一个分解使得$M=U\sum V^{*}$其中U是m×m阶酉矩阵；$\sum$是m×n阶非负实数对角矩阵；而$V^{*}$，即V的共轭转置，是n×n阶酉矩阵。这样的分解就称作$M$的奇异值分解。

### 几何解释

首先，我们来看一个只有两行两列的简单矩阵。第一个例子是对角矩阵![log00](http://img.blog.csdn.net/20170225201907278?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdG91cmlzdG1hbjU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)从几何的角度，矩阵可以描述为一个变换：用矩阵乘法将平面上的点（x, y）变换成另外一个点（3x, y）：

![log01](http://img.blog.csdn.net/20170225201947559?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdG91cmlzdG1hbjU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)这种变换的效果如下：平面在水平方向被拉伸了3倍，在竖直方向无变化。![log02](http://img.blog.csdn.net/20170225202039887?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdG91cmlzdG1hbjU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

$2*2$矩阵奇异值分解的几何实质是：对于任意$2*2$矩阵，总能找到某个正交网格到另一个正交网格的转换与矩阵变换相对应。

用向量解释这个现象：选择适当的正交的单位向量$v_1$和$v_2$，向量$Mv_1$和$Mv_2$也是正交的。![log05](http://img.blog.csdn.net/20170225201208758?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdG91cmlzdG1hbjU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

奇异值分解的魅力在于任何矩阵都可以找到奇异值。

参考链接：

1. <http://www.ams.org/samplings/feature-column/fcarc-svd>
2. <https://www.cnblogs.com/LeftNotEasy/archive/2011/01/19/svd-and-applications.html>
