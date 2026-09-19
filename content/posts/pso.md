---
title: "全局优化算法之粒子群算法"
date: 2017-02-05
categories: ["数理统计"]
tags: ["优化算法"]
description: "全局优化算法又称现代启发式算法，是一种具有全局优化性能、通用性强且适合于并行处理的算法。这种算法一般具有严密的理论依据，而不是单纯凭借专家经验，理论上可以在一定的时间内找到最优解或近似最优解。"
url: "/全局搜索算法之粒子群算法.html"
math: true
---

## 序言

  前面讨论过一些迭代算法，包括牛顿法、梯度方法、共轭梯度方法和拟牛顿法，能够从初始点出发，产生一个迭代序列。很多时候，迭代序列只能收敛到局部极小点。因此，为了保证算法收敛到全局最小点，有时需要在全局极小点附近选择初始点。此外，这些方法需要计算目标函数。

  全局优化算法又称现代启发式算法，是一种具有全局优化性能、通用性强且适合于并行处理的算法。这种算法一般具有严密的理论依据，而不是单纯凭借专家经验，理论上可以在一定的时间内找到最优解或近似最优解。遗传算法属于智能优化算法之一。

  常用的全局优化算法有： 遗传算法 、模拟退火算法、禁忌搜索算法、粒子群算法、蚁群算法。

## PSO算法

  粒子群算法（Particle swarm optimization）是由James Kennedy &[Russell Eberhart](http://www.engr.iupui.edu/~eberhart/)提出。区别于上节讨论的模拟退火算法，粒子群算法并不是只更新单个迭代点，而是更新一组迭代点，称为群。群中每个点称为粒子。可将群视为一个无序的群体，其中的每个成员都在移动，意在形成聚集，但移动方向是随机的。

  具体来说，求取目标函数在$\mathbb{R}^n$上极小点的过程。

1. 在$\mathbb{R}^n$随机产生一组数据点，为每个点赋予一个速度，构成一个速度向量。这些点视为粒子所在的位置，以指定速度在运动。
2. 针对每个数据点计算对应的目标函数值，基于计算结果，产生一组新的数据点，赋予新的运动速度。

  其每个粒子都持续追踪到目前为止最好的位置，称到目前为止最好的位置为Pbest，全局最好为止Gbest。基于粒子的个体最好位置和群的群的全局最优位置，调整各粒子的运动速度，实现粒子的“交互“。即在每次迭代中，产生两个随机数，分别作为pbest和gbest的权重，以此构成pbest和gbest的一个组合值，分别称为速度项和随机项，再加上加权后的原有速度，可以实现对原有速度的更新。

  目标函数在$\mathbb{R}^n$中，由种群数m组成粒子群，其中第i个粒子在d维的位置为$x_{id}$，其飞行速度为$v_{id}$，该粒子当前搜索的最优位置为，整个粒子群当前位置为，更新公式如下：$$v_{id}^{t+1}=v_{id}^{t}+c_1r_1(P_{id}-x_{id}+c_2r_2(P_{gd}-x_{id}))\quad (1) \ x_{id}^{t+1}=x_{id}{t}+v_{id}^{t+1} \quad \quad(2)$$

$r_1、r_2$是服从U(0,1)分布的随机数，学习因子$c_1、c_2$为非负常数，通常取$c_1=c_2=2$，$v_id \in [v_{min},v_{max}],v_{max}$是自设定的常数，迭代终止条件为预设的最大迭代数或预定的最小适应度阈值。

Matlab代码示例：

```matlab
%% 该代码为基于PSO的函数极值寻优
%
%% 清空环境
clc
clear

%% 参数初始化
%粒子群算法中的两个参数
c1 = 1.49445;
c2 = 1.49445;

maxgen=500;   % 进化次数  
sizepop=100;   %种群规模

Vmax=1;
Vmin=-1;
popmax=5;
popmin=-5;

%% 产生初始粒子和速度
for i=1:sizepop
    %随机产生一个种群
    pop(i,:)=5*rands(1,2);    %初始种群
    V(i,:)=rands(1,2);  %初始化速度
    %计算适应度
    fitness(i)=fun(pop(i,:));   %染色体的适应度
end

%% 个体极值和群体极值
[bestfitness bestindex]=min(fitness);
zbest=pop(bestindex,:);   %全局最佳
gbest=pop;    %个体最佳
fitnessgbest=fitness;   %个体最佳适应度值
fitnesszbest=bestfitness;   %全局最佳适应度值

%% 迭代寻优
for i=1:maxgen
    
    for j=1:sizepop
        
        %速度更新
        V(j,:) = V(j,:) + c1*rand*(gbest(j,:) - pop(j,:)) + c2*rand*(zbest - pop(j,:));
        V(j,find(V(j,:)>Vmax))=Vmax;
        V(j,find(V(j,:)<Vmin))=Vmin;
        
        %种群更新
        pop(j,:)=pop(j,:)+0.5*V(j,:);
        pop(j,find(pop(j,:)>popmax))=popmax;
        pop(j,find(pop(j,:)<popmin))=popmin;
        
        %适应度值
        fitness(j)=fun(pop(j,:)); 
   
    end
    
    for j=1:sizepop
        
        %个体最优更新
        if fitness(j) < fitnessgbest(j)
            gbest(j,:) = pop(j,:);
            fitnessgbest(j) = fitness(j);
        end
        
        %群体最优更新
        if fitness(j) < fitnesszbest
            zbest = pop(j,:);
            fitnesszbest = fitness(j);
        end
    end 
    yy(i)=fitnesszbest;    
        
end
%% 结果分析
plot(yy)
title('最优个体适应度','fontsize',12);
xlabel('进化代数','fontsize',12);ylabel('适应度','fontsize',12);
```

参考论文：

1. An introduction to optimization-最优化导论[J]. Edwin K.P.Chong.
2. [一种更简化更高效的粒子群算法](http://www.jos.org.cn/1000-9825/18/861.pdf)
