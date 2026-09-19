---
title: "Schwarz不等式知识归纳"
date: 2018-06-10
categories: ["数学"]
tags: ["Mathematic"]
description: "Schwarz 不等式是个应用广泛的不等式，常见于线性代数的内积空间，数学分析的无穷级数，连续函数的积分以及概率论中的方差、协方差。"
url: "/Schwarz不等式知识归纳.html"
math: true
---

Schwarz 不等式是个应用广泛的不等式，常见于线性代数的内积空间，数学分析的无穷级数，连续函数的积分以及概率论中的方差、协方差。

一般表述为

$\vert \langle x,y\rangle \vert ^2 \leq \langle x,x\rangle \dot \langle y,y \rangle$

在欧几里得空间$\mathcal{R^n}$中，$$(\sum_{i=1}^{n}x_i y_i)^2 \leq (\sum_{i=1}^{n}x_i^2)(\sum_{i=1}^{n}y_i^2)$$

$$\vert \int f^*(x)g(x)dx \vert ^2 \leq \int \vert f(x) \vert ^2dx \dot \int \vert g(x) \vert ^2dx$$

复向量空间 $\mathbb{C}^n$ 中，考虑两个向量 $x=(x_1,\ldots,x_n),y=(y_1,\ldots,y_n)$将 Schwarz 不等式两边平方并使用标准向量内积，可得$$\vert \sum_{i=1}^{n}\overline{x_i}{y_i}\vert ^2\leq \sum_{i=1}^{n}\vert x_i\vert ^2\cdot\sum_{j=1}^n\vert y_i\vert^2$$上面的式子描述了数列乘积之和与数列平方和乘积的 Cauchy 不等式。由于上式与 Schwarz 不等式本质上相同，故我们经常将上式称作 **Cauchy-Schwarz** 不等式。现在考虑我们熟悉的区间 $[0,1]$上的连续函数空间，Schwarz 不等式形式可以表达成,

$$\vert \int_0^1 \bar{f(t)}g(t) dt \vert^2 \leq \int_0^1 \vert f(t) \vert ^2dt \dot \int_0^1 g(t) \vert ^2dt$$

在一般的广义向量空间，我们定义二向量 $x$ 和 $y$ 的距离为

$$d(\mathbf{x},\mathbf{y})=\vert \mathbf{x}-\mathbf{y} \Vert = \sqrt{\langle\mathbf{x}-\mathbf{y},\mathbf{x}-\mathbf{y} \rangle}$$

注意，$d$ 称作向量范数，需要满足以下三个性质：

1. $d(\mathbf{x},\mathbf{y})=d(\mathbf{y},\mathbf{x})$
2. $d(\mathbf{x},\mathbf{y})\geq 0$ ，当且仅当 $\mathbf{x}=\mathbf{y} $时，$d(\mathbf{x},\mathbf{y})=0$。
3. $d(\mathbf{x},\mathbf{y})\leq d(\mathbf{x},\mathbf{z})+d(\mathbf{z},\mathbf{y})$

显然，向量范数 满足(1) 和 (2)，性质 (3) 即为三角不等式，此式可由 Schwarz 不等式导出，如下：

### 关于证明

可参考：[以 Bessel 不等式证明 Schwarz 不等式](https://ccjou.wordpress.com/2010/03/10/schwarz-%E4%B8%8D%E7%AD%89%E5%BC%8F/)

### 延伸点

从数学分析到泛函分析里最重要的一些不等式:

- Schwarz不等式
- Jesen不等式（凸分析与随机数学中出现得比较多）
- 赫尔德（Holder）不等式
- 闵可夫斯基（Minkowski）不等式
- Hilbert空间的贝塞尔不等式
- Poincare不等式（变分学中非常重要的不等式）
- Soblev空间嵌入定理（在变分学和偏微分方程中非常重要的不等式）

以上这些不等式，是必须记住、经常用到（不仅仅在数学自身学科中用到）的最基本的不等式。

结合运筹学与控制论方向，顺便说一说必须牢牢记住的、最常用的**分析学**定理:

- Banach不动点定理
- Hilbert空间的投影定理
- Hahn-Banach定理（核心中的核心）与分离超平面定理
- 反函数定理和隐函数定理（赋范线性空间的微分学）
- 阿尔采拉-阿斯科利定理
- Sobolev嵌入定理
- Rellich Kontracheev紧嵌入定理
- Eblerlin Schulyman定理
- Lagrange乘子定理
- Kuhn-Tucker定理（无限维空间的版本，基于Hahn-Banach定理）
- Pontryagin最大值原理（利用Frechet微分理论和前面的乘子定理去理解即可）
- Brouwer（布劳威尔）不动点定理
- Schaulder（绍德）不动点定理

### 复变函数中的柯西不等式

设 $ f(z)$ 在区域 $D$ 及其边界上解析，$a$ 为 $D$ 内一点，以 $a$ 为圆心做圆周 $C_R: |z-a|=R$，只 $C_R$ 及其内部 $G$ 均被 $D$ 包含，则有：

$$\vert f^{(n)}(z_0) \vert \leq \frac{n!M}{R^n}$$

其中，$M$ 是 $\vert f(z) \vert$ 的最大值，$M= \max \vert f(x) \vert$

### 其它推广

$$\sqrt {\sum _{i=1}^{n} (\sum _{j=1}^{m} a_{ij})^2} \leq \sum _{j=1}^{m} \sqrt {\sum _{i=1}^{n}a_{ij}^2} \\ m \req \alpha > 0,(\sum _{i=1}^{n} \prod _{j=1}^{m} a_{ij})^{\alpha }\leq \prod _{j=1}^{m}\sum _{i=1}^{n} a_{ij}^\alpha$$
