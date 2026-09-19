---
title: "用Tensorflow写简单的神经网络"
date: 2017-02-25
categories: ["机器学习相关"]
tags: ["Python", "Machine-Learning", "TensorFlow"]
url: "/用Tensorflow写简单的神经网络.html"
---

TensorFlow是一个采用数据流图（data flow graphs），用于数值计算的开源软件库。节点（Nodes）在图中表示数学操作，图中的线（edges）则表示在节点间相互联系的多维数据数组，即张量（tensor）。它灵活的架构让你可以在多种平台上展开计算，例如台式计算机中的一个或多个CPU（或GPU），服务器，移动设备等等。

![log00](http://tensorfly.cn/images/tensors_flowing.gif)

根据上图，可以看出一个简单神经网络所具有的模块结构，首先输入层(Input Layer)，接受相关的结构化化数据；其次是隐藏层(Hidden Layer)，隐藏层主要加权运算，通过激活函数达到拟合线性非线性函数的目的；最后有输出层(Output Layer)，其结果成为下一次迭代的初始值。

一个的单层神经网络如下：![log01](http://hahack.com/images/ann2/w4eQd.png)

就此，我们用Tensorflow实现一个单层神经网络，参考代码如下：

```python
#!/usr/bin/python  
# -*- coding: utf-8 -*-  
from __future__ import print_function
import tensorflow as tf
import numpy as np

# 定义神经网络层
def add_layer(inputs,in_size,out_size,activation_function=None):
    Weights = tf.Variable(tf.random_normal([in_size,out_size]))
    biases = tf.Variable(tf.zeros([1,out_size])+0.1)
    Wx_plus_b = tf.matmul(inputs,Weights)+biases
    
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs

# 定义数据
x_d = np.linspace(-1,1,300)[:,np.newaxis]
noise = np.random.normal(0,0.05,x_d.shape)
y_d = np.square(x_d) - 0.5 + noise

# 定义placeholder，可以更方便
xs = tf.placeholder(tf.float32,[None,1])
ys = tf.placeholder(tf.float32,[None,1])

# 添加隐藏层
layer1 = add_layer(xs,1,10,activation_function = tf.nn.relu)
predict = add_layer(layer1,10,1,activation_function = None)

# 定义损失函数
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - predict),reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.3).minimize(loss)

# 初始化
# init = tf.initialize_all_variables() no long valid from
# 2017-03-02 if using tensorflow >= 0.12

if int((tf.__version__).split('.')[1]) < 12:
    init = tf.initialize_all_variables()
else:
    init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

# 输出结果
for i in range(1000):
    # 训练
    sess.run(train_step, feed_dict={xs: x_d, ys: y_d})
    if i % 50 == 0:
        # to see the step improvement
        print(sess.run(loss, feed_dict={xs: x_d, ys: y_d}))
```

单机运行结果如下：![log2](http://img.blog.csdn.net/20170225020607154?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdG91cmlzdG1hbjU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

> [1]参考链接：<https://www.youtube.com/watch?v=S9wBMi2B4Ss&list=PLXO45tsB95cKI5AIlf5TxxFPzb-0zeVZ8&index=13>
