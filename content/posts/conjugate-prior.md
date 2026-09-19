---
title: "共轭先验"
date: 2017-02-18
categories: ["数理统计"]
tags: ["统计学", "Mathematic"]
url: "/共轭先验.html"
math: true
---

> 定义：如果先验分布和似然函数可以使得先验分布和后验分布有相同的形式，那么就称先验分布与似然函数是共轭的。

读数理统计学导论时，遇到过共轭先验的概念。  贝叶斯判别准则中，分别假设了先验分布$p(\theta)$，后验分布$p(\theta|X)$，以及$p(X), p(X|\theta)$似然函数。

贝叶斯定理可以写作：$$P(\theta|X)=\frac{P(\theta)P(X|\theta)}{P(X)}$$

即 「后验分布 =先验分布 * 似然函数 / P(X)」

  之所以采用共轭先验的原因是可以使得先验分布和后验分布的形式相同，这样一方面合符人的直观（它们应该是相同形式的；另外一方面是可以形成一个先验链，即现在的后验分布可以作为下一次计算的先验分布，如果形式相同就可以形成一个链条。为了使得先验分布和后验分布的形式相同，我们定义：如果先验分布和似然函数可以使得先验分布和后验分布有相同的形式，那么就称先验分布与似然函数是共轭的。所以共轭是指：先验分布和似然函数共轭。

### 例子：

共轭先验通常可以由分布的pdf或pmf来确定。

考虑二项模型：$$p(x)={n \choose x}q^{x}(1-q)^{n-x}$$

写成以q为参数的函数形式：$$f(q)\propto q^{a}(1-q)^{b}$$

通常这个函数应该还缺少一个乘数因子，以保证pdf的积分值为1。

这个乘数项是a，b的函数。写作下面的形式$$p(q)={q^{\alpha -1}(1-q)^{\beta -1} \over \mathrm {B} (\alpha ,\beta )}$$

可以看出，乘上的$\mathrm {B} (\alpha ,\beta )$作为归一化常熟存在，根据上面定义，可得二项分布的共轭分布族是**贝塔分布。**

  与共轭先验对应的概念是共轭分布族(Conjugate family of distribution),所谓共轭分布族是指参数$\theta$的后验pdf与作为先验的分布族是相同的，则称此类先验pdf关于具有pdf$f(x|\theta),\theta \in \Omega$的分布族为共轭分布。

  例如，给定$\theta$时随机变量X的pmf是均值为$\theta$的泊松分布。若我们选取伽马先验，由贝叶斯定理计算出后验也是伽马分布族。则称，伽马分布族构成这种泊松模型的共轭先验类。

> 一般而言，有了先验和似然，计算后验能够方便我们实现变分推断和Gibbs采样等

参考资料：

1. Pattern Recognition and Machine Learning , M. Bishop
2. 数理统计学导论 ,Robert V.Hogg
3. Conjugate prior - Wikipedia
4. [以贝塔分布为例，解释了共轭分布，并给出了R语言的code.](https://link.zhihu.com/?target=https%3A//alexanderetz.)com/2015/07/25/understanding-bayes-updating-priors-via-the-likelihood/
