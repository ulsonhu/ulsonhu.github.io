---
title: "Note-关于事件的运算"
date: 2018-04-20
categories: ["Note"]
tags: ["数理统计", "Mathematic"]
description: "Note系列为日常笔记。"
url: "/Note-关于事件的运算.html"
math: true
---

## 关于事件的运算

$$\underset{n \rightarrow \infty}{\overline{lim}} A_n= \bigcap _{k=1}^{\infty} \bigcup _{n=k}^{\infty} A_n$$

$$\underset{n \rightarrow \infty}{\underline{lim}} A_n= \bigcup _{k=1}^{\infty} \bigcap _{n=k}^{\infty} A_n$$

其中，$\underset{n \rightarrow \infty}{\overline{lim}} A_n​$ 为事件序列$\{A_n\}​$的上限事件，表示$A_n​$发生无穷多次。类似的，称 $\underset{n \rightarrow \infty}{\underline{lim}} A_n​$ 为事件序列的下限事件，表示$A_n​$之多只有有限个不发生。

显然，有$$\underset{n \rightarrow \infty}{\overline{lim}} A_n \supset \underset{n \rightarrow \infty}{\underline{lim}} A_n$$

特别的，当$\underset{n \rightarrow \infty}{\overline{lim}} A_n = \underset{n \rightarrow \infty}{\underline{lim}} A_n$ 时，记 $ \underset{n \rightarrow \infty}{lim} A_n \equiv \underset{n \rightarrow \infty}{\overline{lim}} A_n = \underset{n \rightarrow \infty}{\underline{lim}} A_n$，并称它为事件序列$\{A_n\}$的极限事件。

由德摩根定律，有

$$\overline{(\bigcap _{k=1}^{\infty} \bigcup _{n=k}^{\infty} A_n)}=\bigcup _{k=1}^{\infty} \bigcap _{n=k}^{\infty} \overline{A_n}$$

$$\overline{(\bigcup _{k=1}^{\infty} \bigcap _{n=k}^{\infty} A_n)}=\bigcap _{k=1}^{\infty} \bigcup _{n=k}^{\infty} \overline{A_n}$$

因此$$\underset{n \rightarrow \infty}{\underline{lim}} \overline{A_n} = \overline{(\underset{n \rightarrow \infty}{\overline{lim}} A_n)}$$$$\underset{n \rightarrow \infty}{\overline{lim}} \overline{A_n} = \overline{(\underset{n \rightarrow \infty}{\underline{lim}} A_n)}$$

由此引出的$\text{Borel-Cantelli}$引理，在概率论中有着众多应用。

$\text{Borel-Cantelli lemma}$:

1. 若随机事件序列$\{A_n\}$满足$$\sum_{n=1}^{\infty}P(A_n)<\infty$$则$$P\{ \underset{n \rightarrow \infty}{\overline{lim}} A_n\}=0, P\{ \underset{n \rightarrow \infty}{\underline{lim}} \overline{A_n}\}=1$$
2. 若$\{A_n\}$是相互独立的随机事件序列，则$$\sum_{n=1}^{\infty}P(A_n)=\infty$$的充要条件为

   $$P(\underset{n \rightarrow \infty}{\overline{lim}} A_n)=1 \text{ or } P(\underset{n \rightarrow \infty}{\underline{lim}} \overline{A_n})=0 ​$$

由此，我们可以进一步讨论以概率1收敛.

$$\xi_n(\omega) \overset{a.s.}{\rightarrow} \xi (\omega)$$
