---
title: "HMM-隐马尔可夫模型"
date: 2018-04-01
categories: ["数理统计"]
tags: ["统计学", "数理统计"]
description: "隐马尔可夫模型（Hidden Markov Model，$\\text{HMM}$）是统计模型，它用来描述一个含有隐含未知参数的马尔可夫过程。其难点是从可观察的参数中确定该过程的隐含参数。然后利用这些参数来作进一步的分析，例如模式识别。"
url: "/HMM-隐马尔可夫模型.html"
math: true
---

## 马尔科夫链

在介绍$\text{HMM}$之前，我们先要了解什么是马尔科夫链。马尔科夫链是一个随机过程，简单来说就是当前时刻的状态与前 $p$ 个时刻的状态有关，即

$$P(z(t) | z(t-1),z(t-2),\cdots,z(1),z(0)) = P(z(t)|z(t-1),z(t-2),\cdots,z(t-p))$$

这种被称作 $p$ 阶马尔科夫链；为了简化这个过程以方便应用到模型中，我们有两个假设：

- 在序列中，当前时刻状态只依赖于前一时刻的状态，也就是$P(z(t)|z(t-1), z(t-2),\cdots, z(1), z(0)) = P(z(t)|z(t-1))$。
- 状态转移的分布不随时间的改变而改变，也就是说任意时刻下的状态产生与时间无关，仅仅与前一状态有关。

但是实际生活中，这种状态本身是很难观测到的，我们只能根据其他的特征来观测这些状态，同时状态之间的 **转移矩阵**也是很难直接获得的，这就需要隐马尔科夫模型了.

## HMM 形象的例子描述

在引入$\text{HMM}$的公式化描述之前，为了更好的理解 HMM 模型，我们先用一个掷骰子的例子来形象的描述 HMM模型.

模型描述假设我手里有三个不同的骰子。

- 第一个骰子是我们平常见的骰子（称这个骰子为D6），6个面，每个面$（1，2，3，4，5，6）$出现的概率是1/6。
- 第二个骰子是个四面体（称这个骰子为D4），每个面$（1，2，3，4）$出现的概率是1/4。
- 第三个骰子有八个面（称这个骰子为D8），每个面$（1，2，3，4，5，6，7，8）$出现的概率是1/8。

![](https://res.cloudinary.com/ulsonhu/image/upload/v1523585401/2018_04_10-4.png)

假设我们开始掷骰子，我们先从三个骰子里挑一个，挑到每一个骰子的概率都是1/3。然后我们掷骰子，得到一个数字，$1，2，3，4，5，6，7，8$中的一个。不停的重复上述过程，我们会得到一串数字，每个数字都是$1，2，3，4，5，6，7，8$中的一个。例如我们可能得到这么一串数字（掷骰子10次）：$1 6 3 5 2 7 3 5 2 4$

这串数字叫做**可见状态链**。但是在隐马尔可夫模型中，我们不仅仅有这么一串可见状态链，还有一串**隐含状态链**。在这个例子里，这串隐含状态链就是你用的骰子的序列。比如，隐含状态链有可能是：D6 D8 D8 D6 D4 D8 D6 D6 D4 D8

一般来说，$\text{HMM}$中说到的马尔可夫链其实是指隐含状态链，因为隐含状态（骰子）之间存在转换概率（transition probability）。在我们这个例子里，D6的下一个状态是D4，D6，D8的概率都是1/3。D4，D8的下一个状态是D4，D6，D8的转换概率也都一样是1/3。这样设定是为了最开始容易说清楚，但是我们其实是可以随意设定转换概率的。比如，我们可以这样定义，D6后面不能接D4，D6后面是D6的概率是0.9，是D8的概率是0.1。这样就是一个新的$\text{HMM}$。

同样的，尽管可见状态之间没有转换概率，但是隐含状态和可见状态之间有一个概率叫做**输出概率**（emission probability）。就我们的例子来说，六面骰（D6）产生1的输出概率是1/6。产生2，3，4，5，6的概率也都是1/6。我们同样可以对输出概率进行其他定义。比如，我有一个被赌场动过手脚的六面骰子，掷出来是1的概率更大，是1/2，掷出来是2，3，4，5，6的概率是1/10。

![](https://res.cloudinary.com/ulsonhu/image/upload/v1523584361/2018_04_10-1.png)隐马尔可夫示意图

其实对于 $\text{HMM}$ 来说，如果提前知道所有隐含状态之间的转换概率和所有隐含状态到所有可见状态之间的输出概率，做模拟是相当容易的。

但是应用$\text{HMM}$模型时候呢，往往是缺失了一部分信息的，有时候你知道骰子有几种，每种骰子是什么，但是不知道掷出来的骰子序列；有时候你只是看到了很多次掷骰子的结果，剩下的什么都不知道。如果应用算法去估计这些缺失的信息，就成了一个很重要的问题。

## HMM模型解决的三个问题

1. 知道骰子有几种（隐含状态数量），每种骰子是什么（转换概率），根据掷骰子掷出的结果（可见状态链），我想知道每次掷出来的都是哪种骰子（隐含状态链）

> 这个问题呢，在语音识别领域呢，叫做 **解码问题**。这个问题其实有两种解法，会给出两个不同的答案。每个答案都对，只不过这些答案的意义不一样。
>
> - 第一种解法求最大似然状态路径，说通俗点呢，就是我求一串骰子序列，这串骰子序列产生观测结果的概率最大。
> - 第二种解法呢，就不是求一组骰子序列了，而是求每次掷出的骰子分别是某种骰子的概率。比如说我看到结果后，我可以求得第一次掷骰子是D4的概率是0.5，D6的概率是0.3，D8的概率是0.2

2. 还是知道骰子有几种（隐含状态数量），每种骰子是什么（转换概率），根据掷骰子掷出的结果（可见状态链），我想知道掷出这个结果的概率

看似这个问题意义不大，因为你掷出来的结果很多时候都对应了一个比较大的概率。问这个问题的目的呢，其实是检测观察到的结果和已知的模型是否吻合。如果很多次结果都对应了比较小的概率，那么就说明我们已知的模型很有可能是错的，有人偷偷把我们的骰子給换了

3. **知道骰子有几种（隐含状态数量），不知道每种骰子是什么（转换概率），观测到很多次掷骰子的结果（可见状态链），我想反推出每种骰子是什么(转换概率)**

> 这个问题很重要，因为这是最常见的情况。很多时候我们只有可见结果，不知道$\text{HMM}$模型里的参数，我们需要从可见结果估计出这些参数，这是建模的一个必要步骤

在实际应用中，比如中文分词，我们更多的是利用**第三个问题**去建模( 当然，如果利用工具的话，你拿到手的时候这部分的参数都是已经训练好了的 )，然后用**第一个问题**的解码去求隐含状态序列（这也是我们的目标，比如分词、词性标注等）.

### 破解骰子序列

举例来说，我知道我有三个骰子，六面骰，四面骰，八面骰。我也知道我掷了十次的结果`1 6 3 5 2 7 3 5 2 4`，我不知道每次用了那种骰子，我想知道最有可能的骰子序列

其实最简单而暴力的方法就是穷举所有可能的骰子序列，然后依照第零个问题的解法把每个序列对应的概率算出来。然后我们从里面把对应最大概率的序列挑出来就行了。如果马尔可夫链不长，当然可行。如果长的话，穷举的数量太大，就很难完成了。

另外一种很有名的算法叫做 Viterbi algorithm.

## HMM 的几个要素

经过上面形象化的例子描述，读者应该对隐马尔科夫模型有了大致的了解，下面通过引入数学化描述，来正式介绍 $\text{HMM}$.读者在阅读 $\text{HMM}$ 数学化描述时，可以对照前面掷骰子的问题来理解.

- StatusSet : 状态值集合，常用 $S=\{S_1,S_2,\cdots ,S_Q\}$ 来表示系统的隐状态集合，其中 $Q$ 为隐状态数。用 $q_t=S_i$ 表示系统在时刻 $t$ 处于隐状态 $S_i$，隐状态序列为$Q=\{q_1,q_2,\cdots ,q_t\}$

例如上面的三个不同的骰子，这些状态之间满足马尔科夫性质，是马尔科夫模型中实际所隐含的状态，这些状态通常无法直接观察得到.

- ObservedSet :观察值集合，观测序列记为 $O = (o_1,o_2,\cdots,o_T)$，其中 $T$ 为观测序列的长度； $O_t$为时刻$t$ 的观测随机变量，可以是一个数值或向量.

> 例如上面的 $1,2,3,4,5,\cdots $ 等值，在模型中与隐含状态相关联，可通过直接观测得到.

- TransProbMatrix :转移概率矩阵，状态转移的概率分布可表示为 $A=\{a_{ij}\}$，其中 $a_{ij} = P(q_{t+1} = S_j | q_t = S_i), 1 \leq i,j \leq Q$，且满足$a_{ij} \geq 0,\sum_{j=1}^Q a_{ij} = 1$ ，表示时刻 $t$ 从状态 $a_i$ 状态转移到时刻 $t+1$ 状态 $a_j$ 的概率.

> 例如上面的取不同骰子的概率，描述了 $\text{HMM}$ 模型中各个状态之间的转移概率，

- EmitProbMatrix :发射概率矩阵，假设观测变量的样本空间为$V$ ，在状态 $S_i$ 时输出观测变量的概率分布可表示为:$B = \{ b_i(v),1 \leq i \leq Q,v \in V \}$ ，其中$b_i(v) = f\{ O_t = v | q_t = S_i \}$ 。

> 例如上面的每个骰子取不同值的概率，令 $N$代表隐含状态数目， $M$代表可观测状态数目，则 $B_{ij} = P(O_i | S_j),1 \leq i \leq M,1 \leq j \leq N$ 表示在 $t$ 时刻、隐含状态是$S_j$ 条件下，观察状态为$O_i$ 的概率.

- InitStatus :初始状态分布，一般用 $\pi $ 来表示，即 $\pi = \{ \pi_i,1 \leq i \leq Q \}$，其中 $\pi_i = P\{ q_1 = S_i \}$例如上面我们假设投掷的是第一枚骰子，表示隐含状态在初始时刻 $t=1$ 的概率矩阵.

从定义可知，隐马尔科夫模型作了**两个基本假设:**

- **齐次马尔科夫假设**即假设隐藏的马尔科夫链在任意时刻 的状态只依赖于其前一时刻的状态，与其他时刻的状态及观测无关，也与时刻 无关.$$P(q_t | q_{t-1},o_{t-1},\cdots,q_1,o_1) = P(q_t | q_{t-1}),t = 1,2,\cdots,T$$
- **观测独立性假设**即假设任意时刻的观测只依赖于该时刻的马尔科夫链的状态，与其他观测及状态无关.$$P(o_t | q_T,o_T,q_{T-1},o_{T-1},\cdots,q_{t+1},o_{t+1},q_t,q_{t-1},o_{t-1},\cdots,q_1,o_1) = P(o_t | q_t)$$

## 观测序列的生成过程

上面的例子中我们也大致讲了序列如何生成的，这里我们用数学描述提炼一下：

**输入**: 隐马尔科夫模型 $\lambda=\{A,B,\pi \}$，观测序列长度 $T$;

**输出**: 观测序列 $O = (o_1,o_2,\cdots,o_T)$

- 按照初始状态分布 $\pi$ 产生状态 $q_1$
- 令 $t=1$
- 按照状态 $q_t$ 的观察概率分布 $b_{q_t}(v)$ 生成 $o_t$
- 按照状态 $q_t$ 的状态转移概率分布 $\{q_{ij}\}$ 产生状态 $q_{t+1},q_{t+1} \in \{ S_1,S_2,\cdots,S_Q \}$
- 令 $t=t+1$ ；如果 $t<T$，转步 3；否则，终止.

## $\text{HMM}$ 的基本问题

隐马尔科夫模型在实际中运用，必须解决下面三个基本问题 :

给定观察序列 $O = (o_1,o_2,\cdots,o_T)$ 和模型 $\lambda=\{A,B,\pi \}$，如何有效地计算观测值序列的输出概率?

给定观察值序列和输出该观察值序列的隐马尔科夫模型 ，如何有效确定与之对应的最佳状态序列?即估计出模型产出观察值序列最有可能经过的路径.

对于初始模型和给定用于训练的观察值序列 $O = (o_1,o_2,\cdots,o_T)$，如何调整模型参数$\lambda=\{A,B,\pi \}$ ，使得输出概率最大 $P(O|\lambda)$ ？

Note:对应到上面掷骰子的例子中所说的三个问题

## 基本算法

### 直接计算

给定模型 $\lambda=\{A,B,\pi \}$ 和观测序列 $O = (o_1,o_2,\cdots,o_T)$,计算观测序列 $O$ 出现的概率 $P(O|\lambda)$ . 最直接的方法就是按概率公式直接算：通过列举所有可能的长度为 $T$ 的状态序列 $Q={Q_1,Q_2,\cdots Q_t}$，求各个状态序列 $Q$ 与观测序列 $O = (o_1,o_2,\cdots,o_T)$ 的联合概率$P(O,Q|\lambda)$ ，然后对所有可能的状态序列求和，得到 $P(O|\lambda)$.

状态序列 $Q={Q_1,Q_2,\cdots Q_t}$ 的概率是$$P(Q|\lambda) = \pi_{q_1} a_{q_1 q_2} a_{q_2 q_3} \cdots a_{q_{T-1} q_{T}}$$

对固定的状态序列 $Q={Q_1,Q_2,\cdots Q_t}$, 观测序列 $O = (o_1,o_2,\cdots,o_T)$ 的概率是$$P(O|Q,\lambda) = b_{q_1}(o_1) b_{q_2}(o_2) \cdots b_{q_T}(o_T)$$

则 $O,Q$ 同时出现的联合概率为:$$P(O,Q|\lambda) = P(O|Q,\lambda) P(Q|\lambda) \\ = \pi_{q_1} b_{q_1}(o_1) a_{q_1 q_2} b_{q_2}(o_2) \cdots a_{q_{T-1} q_T} b_{q_T}(o_T) $$

然后，对所有可能的状态序列 $Q$ 求和，得到观测序列 $O$ 的概率 $P(O|\lambda)$ ，即

$$P(O|\lambda) = \sum_{Q} P(O|Q,\lambda) P(Q|\lambda) \\ = \sum_{q_1,q_2,\cdots,q_T} \pi_{q_1} b_{q_1}(o_1) a_{q_1 q_2} b_{q_2}(o_2) \cdots a_{q_{T-1} q_T} b_{q_T}(o_T) $$

但是，该式计算量很大，是 $O(TN^T)$ 阶的，这种算法不可行.

### 前向-后向算法

解决问题 1 的最常用、最有效的方法就是 *Baum* 等人提出的前向-后向算法。

该算法定义**前向概率变量**$$\alpha_t(i) : \alpha_t(i) = P(o_1,o_2,\cdots,o_t,q_t = S_i | \lambda)$$$\alpha(t_i)$ 可由下面递推公式计算得到 :

初始化:$\alpha_1(i) = \pi_i b_i(o_1), 1 \leq i \leq Q$

递推:$$\alpha_{t+1}(j) = [ \sum_{i=1}^Q \alpha_t(i) a_{ij} ] b_j(o_{t+1}) , 1 \leq j \leq Q,1 \leq t \leq T-1$$

结束:$P(O | \lambda) = \sum_{i=1}^Q \alpha_T(i)$

其中$\sum_{i=1}^Q \alpha_T(i)$ 是把最后 $T$ 时刻的所有可能的状态下观察到 $O$ 的概率求和；因为到最后 $T$ 时刻时，每一条状态路径都能观察到观测序列 $O$，且有一个生成概率，即$\alpha_T(i)$，于是将 $T$时刻所有可能的状态对应的前向概率变量累加，就是将所有可能观察到观测序列的状态序列的概率相加，即 $P(O|\lambda)$上述前向算法的递推关系如图所示:

![](https://res.cloudinary.com/ulsonhu/image/upload/v1523584358/2018_04_10-2.png)

与前向算法相似，后向算法是从后向前递推计算输出概率的方法。定义后向概率变量$$\beta_t(i) : \beta_t(i) = P(o_{t+1},o_t,\cdots,o_T | q_t = S_i,\lambda)$$

则 $\beta_t(i)$ 可由下面递推公式计算，后向算法的递推关系图如下所示:

初始化 : $\beta_T(i) = 1, 1 \leq i \leq Q$

递推公式:$$\beta_t(i) = \sum_{j=1}^Q a_{ij} b_j(o_{t+1}) \beta_{t+1}(j), 1 \leq i \leq Q,t = T-1,\cdots,1$$

结束 : $P(O | \lambda) = \sum_{i=1}^Q \beta_1(i) \pi_i = \beta_0(1)$

![](https://res.cloudinary.com/ulsonhu/image/upload/v1523584358/2018_04_10-3.png)

根据前向变量和后向变量的定义，显然下式成立 ：

$$P(O | \lambda) = \sum_{i=1}^Q \sum_{j=1}^Q \alpha_t(i) a_{ij} b_j(o_{t+1}) \beta_{t+1}(j),1 \leq t \leq T-1$$

如何来理解该式子？

$\alpha_t(i) a_{ij} b_j(o_{t+1}) \beta_{t+1}(j)$表示 $t$ 时刻为状态 $q_i$ 的前向概率（根据前向概率的定义，已经计算了 $t$ 时刻状态为 $q_i$ 时观测到 $o_t$ 的概率）， $t$时刻状态 $q_i$ 转移到 $t+1$ 时刻的状态 $q_j$，在 $t+1$ 时刻状态 $q_j$ 下观测到$o_{t+1}$ 的概率，最后乘以 $t+1$ 时刻状态为 $q_j$的后向概率（因为按后向概率的定义不包含当前状态的观察概率 $b_j(o_{t+1})$ 的计算）；分别求所有可能的状态 $q_i,q_j$ 的组合，就是$P(O|\lambda)$ .

利用该算法减少计算量的原因在于每一次计算直接引用前一个时刻的计算结果，避免重复计算.这样，利用前向概率计算 $P(O|\lambda)$ 的计算量是 $O(N^2T)$ 阶的，而不是直接计算的 $O(TN^T)$ 阶.

### 监督学习方法

对于 $\text{HMM}$ 参数估计问题，可按训练数据的特点来分是有监督学习还是无监督学习，如果是有监督学习的话，可直接通过对训练样本做一些统计即可得到 $\text{HMM}$ 的参数估计；在中文自然语言处理中，许多标注问题就是这么做的.

假设已给训练数据包含 $K$ 个长度相同的观察序列和对应的状态序列 ${(O_1,Q_1),(O_2,Q_2),\cdots,(O_K,Q_K)}$，那么我们可以直接利用极大似然估计法来估计隐马尔科夫模型的参数，具体如下:

转移概率 $a_{ij}$ 的估计设样本中时刻 $t$ 处于状态 $q_i$，时刻 $t+1$ 时刻由状态 $q_i$ 转移到了 $q_j$，此种情况出现的频数为 $A_{ij}$ ，那么转移概率$a_{ij}$ 的估计值为

$$\hat{a}_{ij} = \frac{ A_{ij} }{\sum_{j=1}^Q A_{ij} },i = \{S_1,S_2,\cdots,S_Q\};j = \{S_1,S_2,\cdots,S_Q\}$$

即统计由状态 $q_i$ 转移到状态 $q_j$ 占状态 $q_i$ 转移出去的比例.

观测概率 $b_{q_j}(v)$ 的估计设样本中状态为$q_j$ 并观测为 $o_v$ 的频数是 $B_{jv}$，那么状态为 $q_j$ 观测为 $o_v$ 的概率 $b_{q_j}(v)$ 的估计是:

$$\hat{b}_{q_j}(v) = \frac{B_{jv} }{\sum_{v=1}^M B_{jv} }$$

其中，$j = 1,2,\cdots,T;\quad v = 1,2,\cdots,M$.

### Baum-Welch 算法

对于无监督学习的 HMM 参数估计问题，可以使用 Baum-Welch算法.

首先定义两个变量$r_t(i)$ 和$\xi_t(i,j)$ ，给定观察序列 $O(e_1,e_2,\cdots ,e_T)$ 和模型参数 $\lambda=\{A,B,\pi \}$;

- $r_t(i)$为系统在时刻 $t$ 系统处在状态 $S_i$ 的概率，即$$r_t(i) = P(q_t = S_i | O,\lambda)$$
- $\xi_t(i,j)$为 $t$ 时刻状态为 $S_j$ ，到 $t+1$ 时刻系统状态转为 $S_j$ 的概率，即$$\xi_t(i,j) = P(q_t = S_i,q_{t+1} = S_j | O,\lambda)$$

根据前向-后向算法中 $\alpha_t(i)$ 和 $\beta_t(i)$ 定义有:

$$r_t(i) = \frac{\alpha_t(i) \beta_t(i)}{\sum_{j=1}^Q \alpha_t(j) \beta_t(j)},1 \leq i \leq Q \\ \xi_t(i,j) = \frac{\alpha_t(i) a_{ij} b_j(e_{t+1}) \beta_{t+1}(j)}{P(O|\lambda)} \\ \qquad =\frac{\alpha_t(i) a_{ij} b_j(e_{t+1}) \beta_{t+1}(j)}{\sum_{m=1}^Q \sum_{n=1}^Q \alpha_t(m) a_{mn} b_n(e_{t+1}) \beta_{t+1}(n)} ,1 \leq i,j \leq Q$$

则对于观察序列 $O(e_1,e_2,\cdots ,e_T)$ 而言，系统所处于状态 $S_j$ 的总次数（期望值）为 $\sum_{i=1}^Q r_t(i)$ ；同样，系统从状态 $S_i$ 转移到 $S_j$ 的总次数为 $\sum_{i=1}^Q \xi_t(i,j)$ .假设给定训练数据只包含 $K$ 个长度为 $T$ 的观测序列 $\{O_1,O_2,\cdots,O_K \}$ 而没有对应的状态序列，目标是学习隐马尔科夫模型 $\lambda=\{A,B,\pi \}$ 的参数.我们将观测序列数据看作观测数据 $O$，状态序列数据看作不可观测的隐数据 $I$，那么隐马尔科夫模型事实上是一个含有隐变量的概率模型

$$P(O|\lambda) = \sum_{I} P(O|I,\lambda) P(I|\lambda)$$

它的参数学习可以用EM算法来实现.

1. 确定完全数据的对数似然函数所有观测数据写成$O = (o_1,o_2,\cdots,o_T)$ ，所有隐数据写成 $I = (i_1,i_2,\cdots,i_T)$，完全数据是 $(O,I) = (o_1,o_2,\cdots,o_T,i_1,i_2,\cdots,i_T)$，完全数据的对数似然函数是 $\log(P(O,I|\lambda))$
2. EM 算法的 E 步: 求 $Q$ 函数 $Q(\lambda,\overline{\lambda})$$$Q(\lambda,\overline{\lambda}) = \sum_{I} \log \left( P(O,I|\lambda) P(O,I|\overline{\lambda}) \right)$$其中，$\overline{\lambda}$ 是隐马尔科夫模型参数的当前估计值，$\lambda$ 是要极大化的隐马尔科夫模型参数.$$P(O,I|\lambda) = \pi_{i_1} b_{i_1}(o_1) a_{i_1 i_2} b_{i_2}(o_2) \cdots a_{i_{T-1} i_T} b_{i_T}(o_T)$$于是函数 $Q(\lambda,\overline{\lambda})$ 可以写成:$$Q(\lambda,\overline{\lambda}) = \sum_{I} ( \log \pi_{i_1} ) P(O,I|\overline{\lambda}) \\ \sum_{I} ( \sum_{t=1}^{T-1} \log a_{i_t i_{t+1}} ) P(O,I|\overline{\lambda}) + \sum_{I} ( \sum_{t=1}^T \log b_{i_t}(o_t) ) P(O,I|\overline{\lambda})$$式中求和都是对所有训练数据的序列总长度 $T$ 进行的.

> 这其中的 $Q$ 函数，是直接用的《统计学习方法》中的概念，这本书中的 $Q$ 函数比较难懂.

3. EM 算法的 M 步: 极大化 $Q$ 函数 $Q(\lambda,\overline{\lambda})$ 求模型参数 $A,B,\pi$由于要极大化的参数在 $Q(\lambda,\overline{\lambda})$ 中单独地出现在 3 个项中，所以只需对各项分别极大化.

(1). 第一项可以写成:$$\sum_{I} ( \log \pi_{i_1} ) P(O,I|\overline{\lambda}) = \sum_{i=1}^N (\log \pi_i) P(O,i_1 = i | \overline{\lambda})$$注意到 $\pi_i$ 满足约束条件$\sum_{}^N \pi_i = 1$ ，利用拉格朗日乘子法，写出拉格朗日函数:$$L(\pi_i,\gamma) = \sum_{i=1}^N (\log \pi_i) P(O,i_1 = i | \overline{\lambda}) + \gamma ( \sum_{i=1}^N \pi_i - 1 )$$对其求偏导数并令结果为零:$$\frac{\partial L}{\partial \pi_i} = \frac{1}{\pi_i} P(O,i_1 = i | \overline{\lambda}) + \gamma = 0 \\ P(O,i_1 = i | \overline{\lambda}) + \gamma \pi_i = 0 \\ \gamma = -P(O|\overline{\lambda}) \\ \pi_i = \frac{P(O,i_1 = i | \overline{\lambda})}{P(O|\overline{\lambda})}$$

(2). 第 2 项可以写成:$$\sum_{I} ( \sum_{t=1}^{T-1} \log a_{i_t i_{t+1}} ) P(O,I|\overline{\lambda}) \\ = \sum_{i=1}^N \sum_{j=1}^N \sum_{t=1}^{T-1} (\log a_{ij}) P(O,i_t = i,i_{t+1} = j|\overline{\lambda})$$

注意到约束条件 $\sum_{j=1}^N a_{ij} = 1$，应用拉格朗日乘子法得:$$L(a_{ij},\gamma) = \sum_{i=1}^N \sum_{j=1}^N \sum_{t=1}^{T-1} (\log a_{ij}) P(O,i_t = i,i_{t+1} = j|\overline{\lambda}) + \gamma ( \sum_{j=1}^N a_{ij} - 1 )$$求其对 $\alpha_{ij}$ 的偏导，并令其等于零:$$\frac{\partial L}{\partial a_{ij}} = \sum_{t=1}^{T-1} ( \frac{1}{a_{ij}} P(O,i_t = i,i_{t+1} = j|\overline{\lambda}) ) + \gamma = 0 \\ \sum_{t=1}^{T-1} P(O,i_t = i,i_{t+1} = j|\overline{\lambda}) + \sum_{t=1}^{T-1} a_{ij} \gamma = 0$$

对 $j$ 求和:$$\sum_{j=1}^N \sum_{t=1}^{T-1} P(O,i_t = i,i_{t+1} = j|\overline{\lambda}) + \sum_{j=1}^N \sum_{t=1}^{T-1} a_{ij} \gamma = 0 \\ \sum_{t=1}^{T-1} P(O,i_t = i|\overline{\lambda}) + \sum_{t=1}^{T-1} \gamma = 0 \\ a_{ij} = \frac{\sum_{t=1}^{T-1} P(O,i_t = i,i_{t+1} = j | \overline{\lambda})}{\sum_{t=1}^{T-1} P(O,i_t = i|\overline{\lambda})}$$

(3). 第 3 项与第 2 项的计算类似:$$\sum_{I} \left( \sum_{t=1}^T \log b_{i_t}(o_t) \right) P(O,I|\overline{\lambda}) = \sum_{j=1}^N \sum_{t=1}^T \log b_j(o_t) P(O,i_t = j | \overline{\lambda})$$同样用拉格朗日乘子法，约束条件是 $\sum_{k=1}^M b_j(k) = 1$ .注意，只有在 $o_t=v_k$ 时 $b_j(o_t)$ 对 $b_j(k)$ 的偏导数才不为 $0$，以 $I(o_t=v_k)$ 表示，求得$$b_j(k) = \frac{\sum_{t=1}^T P(O,i_t = j | \overline{\lambda}) I(o_t = v_k)}{\sum_{t=1}^T P(O,i_t = j | \overline{\lambda})}$$

#### Note

则上面的概率公式整理一下，并用 $\gamma_t(i),\xi_t(i,j)$ 表示为:$$ a_{ij} = \frac{\sum_{t=1}^{T-1} \xi_t(i,j)}{\sum_{t=1}^{T-1} \gamma_t(i)} \\ b_j(k) = \frac{\sum_{t=1,o_t = v_k}^T \gamma_t(j)}{\sum_{t=1}^T \gamma_t(j)} \\ \pi_i = \gamma_1(i)$$

于是整理 Baum-Welech 完整算法描述如下:

输入：观测数据 $O=(o_1,o_2,\cdots,o_T)$输出：隐马尔科夫模型参数.

- 初始化对 $n=0$，选取 $a_{ij}^{(0)},b_j(k)^{(0)},\pi_i^{(0)}$，得到模型 $\lambda^{(0)} = (A^{(0)},B^{(0)},\pi^{(0)})$
- 递推，对 $n = 1,2,\cdots$$$a_{ij}^{(n+1)} = \frac{\sum_{t=1}^{T-1} \xi_t(i,j)}{\sum_{t=1}^{T-1} \gamma_t(i)} \\ b_j(k)^{(n+1)} = \frac{\sum_{t=1,o_t = v_k}^T \gamma_t(j)}{\sum_{t=1}^T \gamma_t(j)} \\ \pi_i^{(n+1)} = \gamma_1(i) $$右端各值按观测 $O = (o_1,o_2,\cdots,o_T)$ 和模型 $\lambda^{(n)} = (A^{(n)},B^{(n)},\pi^{(n)})$ 计算.
- 终止，得到模型参数 $\lambda^{(n+1)} = (A^{(n+1)},B^{(n+1)},\pi^{(n+1)})$

## R中的HMM

```r
install.packages("HMM")
library(HMM)
```

```r
#后向算法求观察值出现的概率
hmm = initHMM(c("A","B"),c("L","R"),transProbs = matrix(c(0.8,0.2,0.2,0.8),2),emissionProbs = matrix(c(0.6,0.4,0.4,0.6),2))
print(hmm)
# 序列观察值
observations = c("L","L","R","R")
logBackwardProbabilities = backward(hmm,observations)
print(exp(logBackwardProbabilities))
```

```r
# 通过前向算法求观察值出现的概率
hmm = initHMM(c("A","B"), c("L","R"), transProbs=matrix(c(.8,.2,.2,.8),2),
              emissionProbs=matrix(c(.6,.4,.4,.6),2))
print(hmm)
# Sequence of observations
observations = c("L","L","R","R")
# Calculate forward probablities
logForwardProbabilities = forward(hmm,observations)
print(exp(logForwardProbabilities))
```

```r
# 通过Baum-Welch算法训练 hmm参数
hmm = initHMM(c("A","B"),c("L","R"))
transProbs = matrix(c(0.9,0.1,0.1,0.9),2)
emissionProbs = matrix(c(0.5,0.51,0.5,0.49),2)
print(hmm)
a = sample(c(rep("L",100),rep("R",300)))
b = sample(c(rep("L",300),rep("R",100)))
observation = c(a,b)
# Baum-Welch
bw = baumWelch(hmm,observation,10)
print(bw$hmm)
```

```r
# 观察序列最可能出现的概率
hmm = initHMM(c("A","B"), c("L","R"), transProbs=matrix(c(.8,.2,.2,.8),2),
              emissionProbs=matrix(c(.6,.4,.4,.6),2))
print(hmm)
# Sequence of observations
observations = c("L","L","R","R")
# Calculate posterior probablities of the states
posterior = posterior(hmm,observations)
print(posterior)
```

```r
# Viterbi算法解码，求最可能的隐状态序列
# Initialise HMM
hmm = initHMM(c("A","B"), c("L","R"), transProbs=matrix(c(.6,.4,.4,.6),2),
              emissionProbs=matrix(c(.6,.4,.4,.6),2))
print(hmm)
# Sequence of observations
observations = c("L","L","R","R")
# Calculate Viterbi path
viterbi = viterbi(hmm,observations)
print(viterbi)
```

```r
# 训练hmm参数
# Initial HMM
hmm = initHMM(c("A","B"),c("L","R"),
              transProbs=matrix(c(.9,.1,.1,.9),2),
              emissionProbs=matrix(c(.5,.51,.5,.49),2))
print(hmm)
# Sequence of observation
a = sample(c(rep("L",100),rep("R",300)))
b = sample(c(rep("L",300),rep("R",100)))
observation = c(a,b)
# Viterbi-training
vt = viterbiTraining(hmm,observation,10)
print(vt$hmm)
```
