---
title: "指数分布族"
date: 2017-01-23
categories: ["数理统计"]
tags: ["统计学", "Mathematic"]
description: "贝叶斯推断中，要寻找最好的先验分布，其本身是得依据先验数据的。故一个便于运算的策略就是寻找共轭的先验。所谓共轭先验分布就是那些能够导致后验与先验属于同一分布族的先验。而指数族是天生的，具有共轭先验的唯一分布族。"
url: "/指数分布族.html"
math: true
---

指数分布族是指可以表示为指数分布的概率分布。指数分布形式如下：$$P(y;\eta)=b(y)exp(\eta^{T}T(y)-\alpha(\eta))$$其中，$\eta$成为分布的自然参数；$T(y)$是充分统计量，通常$T(y)=y$。当$a、b、T$参数都固定的时候，就定义了一个以 $\eta$ 为参数的指数函数族。

实际上，大多数概率分布都可以表示成上面公式给出的形式：

1. 伯努利分布：对0、1问题进行建模
2. 多项式分布：对K个离散结果的事件建模
3. 泊松分布：对计数过程进行建模
4. 伽马分布与指数分布：对间隔的正数进行建模
5. Beta分布：对小数进行建模
6. Dirichlet分布：对小数进行建模
7. Wishart分布：对协方差进行建模
8. 高斯分布

## 示例

我们将高斯分布与伯努利分布表示成指数分布族的形式。

### 伯努利分布

伯努利分布是对$0、1$问题进行建模，特可以表示成如下形式：

$$P(y;\varphi)=\varphi^y(1-\varphi)^{1-y} \quad y\in{0,1}$$

$$P(y;\varphi) = \varphi^y(1-\varphi)^{1-y} \\=exp(\log \varphi^y(1-\varphi)^{1-y}) \\=exp(y\log \varphi+(1-y)\log(1-\varphi)) \\=exp(y\log \frac{\varphi}{1-\varphi}+\log(1-\varphi))$$

将伯努利分布表示成如下形式，对比指数族分布公示

$$b(y)=1 \\T(y)=1 \\\eta = \frac{\varphi}{1-\varphi} \Rightarrow \varphi=\frac{1}{1+e^{-\eta} } \\\alpha(\eta)=-\log(1-\varphi)=\log(1+e^{\eta})$$

其中可以看到，$\eta$的形式为logistic函数，这是因为logistic模型对问题的先验概率估计是伯努利分布的缘故。

### 高斯分布

  高斯分布可以推导出线性模型，由线性模型的假设函数可知，高斯分布的方差与假设函数无关，因而为简便计算，我们将方差设为1，即使不这样做，最后的结果也是作为一个系数而已，高斯分布转换为指数分布形式的推导过程如下：

![log03](http://img.blog.csdn.net/20170226102549656?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdG91cmlzdG1hbjU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

我们最终一样可以把高斯分布以指数分布族函数的形式表示。

## 后记

1. 这里说明指数分布族的目的，是为了说明关于线性模型(Generalized Linear Model).
2. 凡是符合指数分布族的随机变量，都可以用广义线性模型(GLM)进行分析。

### 备注

指数分布族的**无记忆性**，教科书上所说的无记忆性（Memoryless Property，又称遗失记忆性）。这表示如果一个随机变量呈指数分布，它的条件概率遵循：$$P(T>s+t;T>t)=P(T>s),\quad \text{for all} \quad s,t>0 $$有兴趣的同学可以深入理解一下。
