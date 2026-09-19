---
title: "Lasso回归算法"
date: 2018-03-01
categories: ["数理统计"]
tags: ["统计学", "数量经济学"]
description: "很多人在做变量选择时，眼光依然局限于$R^2$或者$Adjusted-R^2$,以及$P-Value$之中。计量经济学中，对于模型选择，学术界其实更倾向于采用$AIC$和$BIC$等标准来做判断。而对于$P-Value$的滥用与批判，其实已经到了水深火热的地步。抛开背景知识不谈，在变量选择，可以倚靠哪些神奇的准则和方法？"
url: "/LASSO回归算法.html"
math: true
---

[关于P值滥用的简要介绍](http://rokia.org/?tag=p_value)

计量模型中关于变量选择，很多同学可能第一个想到的是：前进法，后退法，向前向后逐步回归。但是，这些方法存在一些固有的缺陷,它们会导致某些可能为最优的变量组合无法共同进入模型。

我们抛开传统的统计学教材，把眼光瞄向统计学习理论，就会发现，其实有大量的模型可供我们选择。今天，先介绍最基础的方法：Lasso。

## 一、The lasso的提出

Lasso,即Lesat absolute shrinkage and seletion operator.改方法由统计学习领域的执牛耳者[Robert Tibshirani于1996年开创](http://statweb.stanford.edu/~tibs/lasso/lasso.pdf)。至今为止，这篇文章被引用次数已达14000多次。据说，在学术领域，被引用次数能达到几十次已经可以引以为傲。经过将近20年的发展，这个方法养活了一大群人，同时也发展出了很多更为成熟的理论，如Adaptive lasso，The Grouped lasso,SCAD。

## 二、The lasso的原理

lasso的思想其实很简单，就是在传统的最小二乘估计上对模型的系数施加一个$L_1$惩罚。模型形式如下。$$\widehat{\beta}^{lasso} =\quad argmin_{\beta}\sum_{i = 1}^{N}(y_i - \beta_0 - \sum_{j = 1}^{p}x_{ij}\beta_j)^2 \\ \qquad s. t\sum_{j = 1}^{p}|\beta_j|\leq t.$$

上式等价于

$$\widehat{\beta}^{lasso} = argmin_{\beta}{\sum_{i = 1}^{N}(y_i - \beta_0 - \sum_{j = 1}^{p}x_{ij}\beta_j)^2 + \lambda\sum_{j = 1}^{p}|\beta_j|}$$

看到这个表达式，有没有一种熟悉的感觉？看！

$$\widehat{\beta}^{ridge} = argmin_{\beta} {\sum_{i = 1}^{N}(y_i - \beta_0 - \sum_{j = 1}^{p}x_{ij}\beta_j)^2 + \lambda\sum_{j = 1}^{p}\beta_{j}^2}$$

没错！它其实跟我们在回归分析教材中常见的岭回归(ridge regression)非常相似，只是将$L_2$惩罚换成了$L_1$惩罚。Zou and Hastie在2005年，提出了一种在ridge regression和the lasso之间折衷的方法：the **elastic net** penalty,思想也非常简单，但是却很有影响力。

回头看下，lasso为何如此流行。这么做的好处是一举多得的：

- 可以解决岭回归能够解决的问题：多重共线性问题,过拟合问题等；
- 还可以解决岭回归不能解决的问题：将一部分变量的系数压缩至0，即实现变量选择。

我们可以从一张图看出来。  
![](https://res.cloudinary.com/ulsonhu/image/upload/v1520764085/2018_03_04p1.png)

这幅图可以这样理解蓝色的区域是$\beta$的可行域。由于the lasso的约束是$L_1$约束，必然是方形区域，区域的大小取决于$t$的大小；而ridge regression是$L_2$约束，所以可行域呈圆形。

$$Z = \sum_{i = 1}^{N}(y_i - \beta_0 - \sum_{j = 1}^{p}x_{ij}\beta_j)^2$$

从上面的式子可以看出，（如果我的空间解析几何没记错的话，）函数$Z(\beta_1,\beta_2)$描述的是一个椭圆抛物面的形状。而椭圆抛物面在$(\beta_1,\beta_2)$平面上的投影就是类似上图红色圆圈所表述的形状，每一圈代表着不同的$Z$值。而中间的黑点，自然就是最小的$Z$，即没有约束下，普通最小二乘得到的解。我们可以想象，当蓝色的圆圈足够大，以至于涵盖了中间的小黑点时，约束没有起到作用，取到的解就是中间的小黑点，此时等价于普通最小二乘；当约束比较紧，取到的解靠近0，为两个区域相切的点。

我们可以直观地看到，the lasso更容易取到角点解，即：使得某些变量的系数压缩至零。如果你还是不相信自己的眼睛，我们待会还可以从一个示例中看出这一特点。

一些爱思考的同学可能会继续追问：“它能够保证留下来的变量都是对因变量有着更大影响的吗？”这一点稍微思考一下，应该是可以保证的。但是，如果存在一组高度相关的变量时，Lasso倾向于选择其中的一个变量，而忽视其他所有的变量。这样可能会导致结果的不稳定性。要解决这个问题，可以去探究一下 **elastic net** penalty。

## 三、lasso的R实现

lasso的实现可以采用glmnet包。glmnet包作者是Friedman, Hastie, and Tibshirani这三位统计学习领域的大牛，可信度无可置疑。这个包采用的算法是循环坐标下降法（cyclical coordinate descent），能够处理的模型包括 linear regression,logistic and multinomial regression models, poisson regression 和 the Cox model，用到的正则化方法就是$l1$范数（lasso）、$l2$范数（岭回归）和它们的混合 （elastic net）。

这里，给出一个实现lasso的示例。

数据来源于ISLR包中的Hitters数据集，该数据集描述了美国1986年和1987年的棒球运动员相关数据。我们来探究一下对运动员薪水起主要作用的因素有哪些。

```r
library(ISLR)
str(Hitters)
```

```r
## 'data.frame':    322 obs. of  20 variables:
##  $ AtBat    : int  293 315 479 496 321 594 185 298 323 401 ...
##  $ Hits     : int  66 81 130 141 87 169 37 73 81 92 ...
##  $ HmRun    : int  1 7 18 20 10 4 1 0 6 17 ...
##  $ Runs     : int  30 24 66 65 39 74 23 24 26 49 ...
##  $ RBI      : int  29 38 72 78 42 51 8 24 32 66 ...
##  $ Walks    : int  14 39 76 37 30 35 21 7 8 65 ...
##  $ Years    : int  1 14 3 11 2 11 2 3 2 13 ...
##  $ CAtBat   : int  293 3449 1624 5628 396 4408 214 509 341 5206 ...
##  $ CHits    : int  66 835 457 1575 101 1133 42 108 86 1332 ...
##  $ CHmRun   : int  1 69 63 225 12 19 1 0 6 253 ...
##  $ CRuns    : int  30 321 224 828 48 501 30 41 32 784 ...
##  $ CRBI     : int  29 414 266 838 46 336 9 37 34 890 ...
##  $ CWalks   : int  14 375 263 354 33 194 24 12 8 866 ...
##  $ League   : Factor w/ 2 levels &quot;A&quot;,&quot;N&quot;: 1 2 1 2 2 1 2 1 2 1 ...
##  $ Division : Factor w/ 2 levels &quot;E&quot;,&quot;W&quot;: 1 2 2 1 1 2 1 2 2 1 ...
##  $ PutOuts  : int  446 632 880 200 805 282 76 121 143 0 ...
##  $ Assists  : int  33 43 82 11 40 421 127 283 290 0 ...
##  $ Errors   : int  20 10 14 3 4 25 7 9 19 0 ...
##  $ Salary   : num  NA 475 480 500 91.5 750 70 100 75 1100 ...
##  $ NewLeague: Factor w/ 2 levels &quot;A&quot;,&quot;N&quot;: 1 2 1 2 2 1 1 1 2 1 ...</code><
```

```r
Hitters<-na.omit(Hitters)
## sampling
x&lt;-model.matrix(Salary~.,Hitters)[,-1]
y&lt;-Hitters$Salary

set.seed(1)
train&lt;-sample(1:nrow(x),nrow(x)/2)
test&lt;-(-train)
y.test&lt;-y[test]

## ridge regression
library(glmnet)
grid&lt;-10^seq(10,-2,length = 100)
ridge.mod&lt;-glmnet(x,y,alpha = 0,lambda = grid)
plot(ridge.mod, main = &quot;The ridge&quot;)
```

![](https://res.cloudinary.com/ulsonhu/image/upload/v1520764084/2018.03_04lasso01.png)

```r
## the lasso
lasso.mod&lt;-glmnet(x[train,],y[train],alpha = 1,lambda = grid)
plot(lasso.mod, main = &quot;The lasso&quot;)
```

![](https://res.cloudinary.com/ulsonhu/image/upload/v1520764084/2018_03_04lasso02.png)

从上面两幅图对比可知，the lasso相比起ridge regression，在压缩变量方便表现更出色。当然，你还可以使用这个包内部的交叉验证函数对(\lambda)进行参数优化，使得模型更具有稳健性。

```plain
## cross-validation
set.seed(1)
cv.out&lt;-cv.glmnet(x[train,],y[train],alpha = 1)
plot(cv.out)
```

![](https://res.cloudinary.com/ulsonhu/image/upload/v1520764084/2018_03_04_lasso03.png)

```r
bestlam&lt;-cv.out$lambda.min
lasso.pred&lt;-predict(lasso.mod,s = bestlam,newx = x[test,])
mean((lasso.pred - y.test)^2)
```

```r
## [1] 100743.4
```

```r
out&lt;-glmnet(x,y,alpha = 1,lambda = grid)
lasso.coef&lt;-predict(out,type = &quot;coefficients&quot;,s = bestlam)[1:20,]
lasso.coef
```

```r
##  (Intercept)        AtBat         Hits        HmRun         Runs 
##   18.5394844    0.0000000    1.8735390    0.0000000    0.0000000 
##          RBI        Walks        Years       CAtBat        CHits 
##    0.0000000    2.2178444    0.0000000    0.0000000    0.0000000 
##       CHmRun        CRuns         CRBI       CWalks      LeagueN 
##    0.0000000    0.2071252    0.4130132    0.0000000    3.2666677 
##    DivisionW      PutOuts      Assists       Errors   NewLeagueN 
## -103.4845458    0.2204284    0.0000000    0.0000000    0.0000000
```

可见，很多变量的系数确实被压缩至零。

## 四、lasso的优缺点分析

- 相比较于其他变量选择方法，如：best subset，Partial Least Squares(偏最小二乘)，Principal components regression(主成分回归)，the lasso和ridge regression对参数的调整是连续的，并不是一刀切的。
- the lasso相比于ridge regression的优势在于压缩变量表现更出色。
- 但是，正如前面所说，lasso还是会有一些潜在的问题，有时候，elastic net等其他的一些lasso的变形会是更好的选择。

## 五、参考文献

1. The Elements of Statistical Learning: Data Mining, Inference and Prediction. Second edition
2. An Introduction to Statistical Learning with R
3. [线性回归建模–变量选择和正则化（1）：R包glmnet](http://site.douban.com/182577/widget/notes/10567212/note/288551448/)
