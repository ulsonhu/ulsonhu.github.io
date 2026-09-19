---
title: "理解异步"
date: 2016-12-20
categories: ["前端"]
tags: ["前端"]
url: "/理解异步.html"
---

JavaScript编程几乎总是伴随着异步操作，传统的异步操作会在操作完成之后，使用回调函数传回结果，而回调函数中则包含了后续的工作。这也是造成异步编程困难的主要原因：

## 前述

**我们一直习惯于“线性”地编写代码逻辑，但是大量异步操作所带来的回调函数，会把我们的算法分解地支离破碎。**

此时我们不能用if来实现逻辑分支，也不能用while/for/do来实现循环，更不用说异步操作之间的组合、错误处理以及取消操作了。因此也就诞生了如jQuery Deferred这样的辅助类库。

我们常见的异步操作：

- 定时器setTimeout
- postmessage
- WebWorkor
- CSS3 动画
- XMLHttpRequest
- HTML5的本地数据
- …

JavaScript要求在与服务器进行交互时要用异步通信，如同AJAX一样。因为是异步模型，所以在调用Transaction游览器提供的本地数据接口时候类似AJAX（这里我是假设），浏览器自己有内部的XHR方法异步处理，但是此时的JS代码还是会同步往下执行，其实就是无阻塞的代码。

**问题：**因为无阻塞，代码在发送AJAX这个请求后会继续执行，那么后续的操作如果依赖这个数据的就会出错了，所以这里就需要等待AJAX返回，才能执行后续操作。

因为异步而导致流程不正确，或者说我们的应用在某个程度上依赖第三方API的数据，那么就会面临一个共同的问题：

我们无法获悉一个API响应的延迟时间，应用程序的其他部分可能会被阻塞，直到它返回结果。Deferreds 的引入对这个问题提供了一个更好的解决方案，它是非阻塞的，并且与代码完全解耦。

当然异步操作也可以提供一个类似于成功回调，失败回调的通知接口。

JS是单线程语言，就简单性而言，把每一件事情（包括GUI事件和渲染）都放在一个线程里来处理是一个很好的程序模型，因为这样就无需再考虑线程同步这些复杂问题。

另一方面，他也暴露了应用开发中的一个严重问题，单线程环境看起来对用户请求响应迅速，但是当线程忙于处理其它事情时，就不能对用户的鼠标点击和键盘操作做出响应。

```javascript
//定时器改变流程
show(1)
setTimeout(function() {
    show(2)}, 0)
show(3)

//执行异步动画
//因为代码的执行是按照从上至下
//但是由于加入了动画，动画形成了异步，所以实际的改变值必须等动画完成才能得到
//但是同步逻辑3其实已经运行，所以3要等待2结束才可以
$("#go").click(function() {
var block = $("#block");
show('1.动画流程代码开始,对象长度'+ block.css('width'))
block.animate({
width       : "70%",
opacity     : 0.4,
marginLeft  : "0.6in",
fontSize    : "3em",
borderWidth : "10px",
}, 1000, function() {
show('2.动画执行结束束,对象长度'+ block.css('width'))
});
show('3.动画流程代码结束,对象长度'+ block.css('width'))
});

function show(data) {
$("body").append('<li>' + data + '</li>')
}
```

## Deferred

### Deferred是什么

前端项目的开发，不仅仅涉及到同步的概念，而且还会经常穿插各种异步的处理。一些大的操作，比如远程获取数据，操作一个大数据处理，这时候是不能马上获取到数据的。假设我们发送一个AJAX请求到接受到数据需要10秒钟，那么从发送到接受数据这个时间段中，前端的处理时间其实是空闲，但是对于开发者来说这种时间是不能浪费了，所以我们可以在10秒钟做很多同步的处理，同时等待异步的数据返回。所以我们需要监听这个回调的数据在成功的时候能够获取到，或者设计一个返回后触发处理的机制，当然原生的JavaScript对这个机制几乎是没有的。为了优化这个形成统一的异步处理方案，jQuery就开始设计了一个Deferred异步模型。

Deferred 提供了一个抽象的非阻塞的解决方案（如异步请求的响应），它创建一个promise对象，其目的是在未来某个时间点返回一个响应。简单来说就是一个异步/同步回调函数的处理方案。

`$.Deferred`在jQuery代码内部有四个模块被使用，分别是“**promise方法”、“DOM ready”、“Ajax模块”及“动画模块**”。

看看jQuery中的最常用的AJAX处理：

**一：Ajax的改造**

传统的jQuery的AJAX操作的传统写法(1.5版之前)：

```javascript
$.ajax({
  url: "aaron.html",
  success: function(){
     alert("成功！");
  },
  error:function(){
    alert("失败！");
  }
})
```

$.ajax()接受一个对象参数，这个对象包含两个方法：success方法指定操作成功后的回调函数，error方法指定操作失败后的回调函数。

在1.5版本后通过新的Deferred引入就改成了：

```javascript
$.ajax("aaron.html")
.done(function(){ alert("成功"); })
.fail(function(){ alert("出错"); });
```

把传参的回调，换成了链式的写法，这样可读性更高了。在jquery 1.5版后，通过$.ajax返回的不是XHR对象了，而是经过包装的Deferred对象，所以就具有promise的一些规范。当然这种写法到底是怎么做的，我们在后续的教程中会详细的讲解到。

**二：提供一种方法来执行一个或多个对象的回调函数**

在实际开发中，我们可能要发送多个异步的请求操作，我们需要等所有的异步都处理完毕后，才能继续下一个动作。

```html
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<script src="http://code.jquery.com/jquery-latest.js"></script>
<title></title>
</head>
<body>
<button id="aaron1">运行案例一</button>
<button id="aaron2">运行案例二</button>
<script type="text/javascript">
//提供一种方法来执行一个或多个对象的回调函数
//在实际开发中，我们可能要发送多个异步的请求操作，我们需要等所有的异步都处理完毕后，才能继续下一个动作
//案例一
function task1(name, fn) {
  setTimeout(function() {
    fn(name)
  }, 500)
}

function task2(name, fn) {
  setTimeout(function() {
    fn(name)
  }, 1000)
}

//任务数
var taskNuns = function() {
  var num = 2; //2个任务
  return function() {
    if (num === 1) {
      show('任务都完成了',$("#aaron1"))
    }
    num--;
  }
}()

$("#aaron1").click(function() {
  //常规处理
  task1('任务一', function() {
    show('task1', $("#aaron1"))
    taskNuns()
  })

  task2('任务二', function() {
    show('task2', $("#aaron1"))
    taskNuns();
  })
})
//========================分割线============================================
//案例二
//通过Deferred改进
function task3(name) {
  var dtd = $.Deferred();
  setTimeout(function() {
    show('task3执行完毕',$("#aaron2"))
    dtd.resolve(name)
  }, 500)
  return dtd;
}

function task4(name) {
  var dtd = $.Deferred();
  setTimeout(function() {
    show('task4执行完毕',$("#aaron2"))
    dtd.resolve(name)
  }, 1000)
  return dtd;
}

$("#aaron2").click(function() {
  $.when(task3('task1'), task4('task2')).done(function() {
    show('when处理成功', $("#aaron2"))
  })
})

function show(data, ele) {
  (ele || $("body")).append('<li>' + data + '</li>')
}
</script>
</body>
</html>
```

所以我们这里要涉及一个等待的处理。我们自己要做一个计时器，每一个任务执行完毕后，都要触发一次任务的检测。当最后一个调用完毕了，我们就可以执行后面的动作，当前这里的写法也会有些问题，比如错误的时候没有处理。同样的功能，我们换成Deferred就会很简单了。

```plain
$.when($.ajax("a1.html"), $.ajax("a2.html"))
　　.done(function(){ alert('2次回调都正确返回了') })
　　.fail(function(){ alert('出错了'); });
```

这段代码的意思是：先执行两个操作

```plain
$.ajax("a1.html")
$.ajax("a2.html")
```

如果都成功了，就运行done()指定的回调函数；如果有一个失败或都失败了，就执行fail()指定的回调函数。

**三：可以混入任意的对象接口中**

jQuery的Deferred最好用的地方，就是模块化程度非常高，可以任意配合使用。

```plain
function task(name) {
  var dtd = $.Deferred();
  setTimeout(function() {
    dtd.resolve(name)
  }, 1000)
  return dtd;
}
$.when(task('任务一'), task('任务二')).done(function() {
  alert('成功')
})
```

把需要处理的异步操作，用Deferred对象给包装一下，然后通过when方法收集异步的操作，最后再返回出done的成功，这样的处理太赞了！

所以说，Deferred的引入，为处理事件回调提供了更加强大并且更灵活的编程模型。

### 认识$.Deferred的接口

大多情况下，promise作为一个模型，提供了一个在软件工程中描述延时（或将来）概念的解决方案。它背后的思想我们已经介绍过：

```plain
不是执行一个方法，然后阻塞应用程序等待结果返回，而是返回一个promise对象来满足未来值。
```

这样看来，Promise/A只是一种规范，Deferred可以看作这种规范的具体实现，旨在提供通用的接口，用来简化异步编程难度，说白了就是:

```plain
一个可链式操作的对象，提供多个回调函数的注册，以及回调列队的回调，并转达任何异步操作成功或失败的消息。
```

jQuery.Deferred()背后的设计理念来自 [CommonJS Promises/A](http://wiki.commonjs.org/wiki/Promises/A) , `jQuery.Deferred()`基于这个理念实现，但并没有完全遵循其设计， 它代表了一种可能会长时间运行而且不一定必须完整的操作的结果，简单的描述下规范中定义的“Promise”。

promise模式在任何时刻都处于以下三种状态之一：

- 未完成（unfulfilled）
- 已完成（resolved）
- 拒绝（rejected）

CommonJS Promise/A 标准这样定义的，promise对象上的then方法负责添加针对已完成和拒绝状态下的处理函数。then方法会返回另一个promise对象，这样可以形成“管道”风格。

看看jQuery的Deferred源码中对动作接口的定义：

```javascript
[ "resolve", "done", jQuery.Callbacks("once memory"), "resolved" ],
[ "reject", "fail", jQuery.Callbacks("once memory"), "rejected" ],
[ "notify", "progress", jQuery.Callbacks("memory") ]
```

Deferred中定义的动作是非常多的，抽象的看其实可以类似一种观察者模式的实现。

观察者模式中的订阅方法：

```plain
Done (操作完成)
Fail (操作失败)
Progress (操作进行中
```

观察中模式中的发布方法：

```plain
resolve（解决）
reject（拒绝）
notify（通知）
```

而且还提供了可以定义运行时的this对象的fire，fireWith，所以扩展了3个可以定义上下文的的接口：

```plain
resolveWith
rejectWith
notifyWith
```

所以按照这样的规范，我们的使用就应该是这样：见代码。

```javascript
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<script src="http://code.jquery.com/jquery-latest.js"></script>
<title></title>
</head>
<body>
<button id="aaron1">例一:基本用法</button>
<button id="aaron2">例二:过滤器</button>
<button id="aaron3">例三:promise方法</button>
<script type="text/javascript">

//例一
$("#aaron1").on("click", function() {
  // 构建一个deferred对象
  var dtd = $.Deferred();
  // 给deferred注册一个成功后的回调通知
  dtd.done(function() {
    show('成功')
  })
  // 开始执行一段代码
  setTimeout(function() {
    dtd.resolve(); // 改变deferred对象的执行状态
  }, 2000);
})

//例二：过滤器
var filterResolve = function() {
  var defer = $.Deferred(),
    filtered = defer.then(function(value) {
      return value * 2;
    });
  defer.resolve(5);
  filtered.done(function(value) {
    show("Value is ( 2*5 = ) 10: " + value);
  });
};
$("#aaron2").on("click", filterResolve)

//例三：实现promise方法
$("#aaron3").on("click", function() {
  var obj = {
    hello: function(name) {
      show("你好 " + name);
    }
  },
    defer = $.Deferred();
  // 设置一个promise
  defer.promise(obj);
  //解决一个deferred
  defer.resolve("慕课网");
  obj.done(function(name) {
    obj.hello(name);
  }).hello("Aaron");
})

function show(data) {
  $("body").append('<li>' + data + '</li>')
}
</script>
</body>
</html>
```

### $.Deferred的设计

由于1.7版本后`$.Callbacks从Deferred`中抽离出去了，目前版本的Deferred.js代码不过150行，而真正$.Deferred的实现只有100行左右，实现的逻辑是相当犀利的。

因为Callback被剥离出去后，整个Deferred就显得非常的精简，代码直接通过extend扩展到静态接口上，对于extend的继承这个东东，在之前就提及过jQuery如何处理内部jQuery与`init`相互引用`this`的问题，所以当`jQuery.extend`只有一个参数的时候，其实就是对jQuery静态方法的一个扩展。

```plain
jQuery.extend({
   Deferred:function(func){
        ...省略代码....
        return deferred
   },
   when:function(func){
      ...省略代码....
      return deferred.promise();
   }
})
```

我们来具体看看2个静态方法内部都干了些什么?

Deferred整体结构：右边代码所示。

Deferred就是一个简单的工厂方法，有两种方式使用：

```javascript
var a = $.Deferred（）
$.Deferred(function(){})
```

内部其实是严重依赖$.Callbacks对象，Callbacks就是用来储存deferred依赖的数据的。

因为done、fail、progress就是jQuery.Callbacks(“once memory”)所有对应的处理：

```javascript
var list = jQuery.Callbacks("once memory")
promise['done'] = list.add;
```

deferred定义了一系列的接口，堪称一绝，100多行的代码，精练的有些过分。

Deferred方法内部建议了2个对象，一个是deferred外部接口对象，一个是内部promise对象。

promise对象解释是一个受限的对象, 这就是所谓的受限制的deferred对象，因为相比之前， 返回的deferred不再拥有resolve(With), reject(With), notify(With)这些能改变deferred对象状态并且执行callbacklist的方法了,只能是then、done、fali等方法。

其内部通过tuples数组，存储了所有的接口API，通过遍历把所有的接口一次都挂到内部promise与deferred对象上。

其中定义了done、fail以及progress这几个方法，其实就是Callbacks回调函数中的add方法，用与push外部的的数据，保存在队列上。

我们通过resolve、reject以及notify其实也就是处理Callbacks中的队列列表。

```javascript
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<script src="http://code.jquery.com/jquery-latest.js"></script>
<title></title>
</head>
<body>
<script type="text/javascript">
// jQuery. Deferred主要处理：
//     显而易见Deferred是个工厂类，返回的是内部构建的deferred对象
//     tuples 创建三个$.Callbacks对象，分别表示成功，失败，处理中三种状态
//     创建了一个promise对象，具有state、always、then、primise方法
//     扩展primise对象生成最终的Deferred对象，返回该对象
//     primise对象就是一个受限对象，只读
var Deferred = function(func) {
  var tuples = [
    //1 动作
    //2 侦听器
    //3 最终状态
    //后面的操作将是围绕这些接口处理
    ["resolve", "done", jQuery.Callbacks("once memory"), "resolved"],
    ["reject", "fail", jQuery.Callbacks("once memory"), "rejected"],
    ["notify", "progress", jQuery.Callbacks("memory")]
  ],
  state = "pending",
  //扩展的primise对象
  promise = {
    state: function() {},
    always: function() {},
    then: function( /* fnDone, fnFail, fnProgress */ ) {},
    promise: function(obj) {}
  },
  deferred = {};
  //定义管道风格的接口pipe
  promise.pipe = promise.then;
  //逐个添加所有的接口到deferred对象上
  jQuery.each(tuples, function(i, tuple) {
    deferred[tuple[0]] = function() {
      deferred[tuple[0] + "With"](this === deferred ? promise : this, arguments);
      return this;
    };
    deferred[tuple[0] + "With"] = list.fireWith;
  });
  //转成成promise对象
  promise.promise(deferred);
  //如果传递的参数是函数，直接运行
  if (func) {
    func.call(deferred, deferred);
  }
  return deferred;
}

//when就是一个合集的处理
//可以收集多个异步操作，合并成功后处理
//同时也可以绑定Promise 对象的其它方法，如 defered.then
//所以when内部必须要创建一个deferred对象
var when = function(subordinate /* , ..., subordinateN */ ) {
  var i = 0,
    resolveValues = slice.call(arguments),
    length = resolveValues.length,
    deferred = remaining === 1 ? subordinate : jQuery.Deferred(),
    updateFunc = function(i, contexts, values) {
      return function(value) {};
    },
    progressValues, progressContexts, resolveContexts;
  if (length > 1) {
    progressValues = new Array(length);
    progressContexts = new Array(length);
    resolveContexts = new Array(length);
    for (; i < length; i++) {
      if (resolveValues[i] && jQuery.isFunction(resolveValues[i].promise)) {
        resolveValues[i].promise()
          .done(updateFunc(i, resolveContexts, resolveValues))
          .fail(deferred.reject)
          .progress(updateFunc(i, progressContexts, progressValues));
      } else {
        --remaining;
      }
    }
  }
  return deferred.promise();
}

</script>
</body>
</html>
```

## Deferred的执行流程

用下面的例子分析（见右侧代码编辑器）：

```javascript
var defer = $.Deferred();
defer.resolve(5);
defer.done(function(value) {})
var filtered = defer.then(function(value) {
  return value * 2;
});
filtered.done(function(value) {});
```

这里有几个关键的问题：

1、defer延时对象通过resolved触发done成功回调，调用在添加done之前，那么靠什么延时处理？

2、为什么defer.then对象返回的给filtered.done的数据可以类似管道风格的顺序叠加给后面的done处理？

一般来说，javascript要实现异步的收集，就需要“等待”，比如defer.resolve(5)虽然触发了，但是done的处理还没添加，我们必须要等待done、then等方法先添加了后才能执行了resolve，那么常规的的用法就是在resolve内部用setTimeout 0，image.onerror行成一个异步的等待操作处理。

但是jQuery很巧妙的绕过了这个收集方式，

defer.resolve(5)方法实际就是触发了callback回到函数的fireWith方法，这样可以接受一个上下文deferred与参数5

```plain
deferred[tuple[0] + "With"](this === deferred ? promise : this, arguments);
```

之前 done | fail | progress方法都是通过jQuery.Callbacks(“once memory”) 或 jQuery.Callbacks(“memory”)生成的。

实际上在Callback源码fire方法有一句 memory = options.memory && data;这样就很巧妙的缓存当前参数5的值，提供给下一个使用，这个就是then，pipe链式数据的一个基础了，此刻的操作，我们把memory保存了这个数据的值。

重点来了，下一个defer.done的操作也是走的add的处理，把done的回调函数加入到list队列中的之后，接着就会触发。

```javascript
 // With memory, if we're not firing then
 // we should call right away
} else if (memory) {
  firingStart = start;
  fire(memory);
}
```

因为memory在上一个resolve操作的时候，缓存了5了，所以memory的判断显示是为真的，所以立刻就触发了fire(memory)的代码了，所以就算触发的循序与添加的循序不一致，也不会导致错误。 而且jquery很巧妙的避免了异步收集的问题，这样处理更可靠了。可见回调函数模块就是为Deferred模块量身定做的了。

第二个问题，是关于then，pipe管道风格的处理，这样也是一个很复杂的设计，在后面一章就提到了。

```javascript
var filterResolve = function() {
  var defer = $.Deferred();
  //先执行成功
  defer.resolve(5);
  //后添加
  defer.done(function(value) {
    $('body').append("<li>defer.done的值是：" + value + "</li>");
  })
  //实现一个管道方法
  var filtered = defer.then(function(value) {
    return value * 2;
  });
  //接受上一个值，叠加处理
  filtered.done(function(value) {
    $('body').append("<li>filtered.done ( 2*5 = ) 10: " + "</li>");
  });
};
$("button").on("click", filterResolve);
```

## Deferred源码剖析(上)

Deferred对接口的设计别出心裁，不是常规的直接定义的，我们可以看tuples这个数组的定义。

**Deferred****自身则围绕这三组数据进行更高层次的抽象**

- 触发回调函数列表执行(函数名)
- 添加回调函数（函数名）
- 回调函数列表（jQuery.Callbacks对象）
- Deferred最终状态（第三组数据除外）

```javascript
var tuples = [
  // action, add listener, listener list, final state
  ["resolve", "done", jQuery.Callbacks("once memory"), "resolved"],
  ["reject", "fail", jQuery.Callbacks("once memory"), "rejected"],
  ["notify", "progress", jQuery.Callbacks("memory")]
]
```

这里抽象出2组阵营：

**1组：回调方法/事件订阅**

`done、fail、progress`

**2组：通知方法/事件发布**`resolve、reject、notify、resolveWith、rejectWith、notifyWith`

Tuples元素集，其实是把相同有共同特性的代码的给合并成一种结构，然后来一次处理。

```javascript
jQuery.each(tuples, function(i, tuple) {
  //代码请看右边代码区域
})
```

对于Tuples的3条数据集是分2部分处理的：

**第一部分将回调函数存入**

```javascript
promise[ tuple[1] ] = list.add;
```

其实就是给promise赋予3个回调函数。

```javascript
promise.done = $.Callbacks("once memory").add
promise.fail = $.Callbacks("once memory").add
promise.progressl = $.Callbacks("memory").add
```

如果存在Deferred最终状态，默认会预先向doneList，failList中的list添加三个回调函数。

```javascript
if (stateString) {
  list.add(function() {
    state = stateString;
  }, tuples[i ^ 1][2].disable, tuples[2][2].lock);
}
```

这里有个小技巧：

[按位异或运算符](https://developer.mozilla.org/zh-CN/docs/JavaScript/Reference/Operators/Bitwise_Operators)

所以实际上第二个传参数是1、0索引对调了，所以取值是failList.disable与doneList.disable。

**通过stateString有值这个条件，预先向doneList,failList中的list添加三个回调函数，分别是:**

```javascript
doneList : [changeState, failList.disable, processList.lock]
failList : [changeState, doneList.disable, processList.lock]
```

changeState 改变状态的匿名函数，deferred的状态，分为三种：pending(初始状态), resolved(解决状态), rejected(拒绝状态)；不论deferred对象最终是resolve（还是reject），在首先改变对象状态之后，都会disable另一个函数列表failList(或者doneList)；然后lock processList保持其状态，最后执行剩下的之前done（或者fail）进来的回调函数。

所以第一步最终都是围绕这add方法：

- done/fail/是list.add也就是[callbacks.add](http://www.cnblogs.com/snandy/archive/2012/11/15/2770237.html#add)，将回调函数存入回调对象中。

**第二部分很简单，给Deferred对象扩充6个方法：**

- resolve/reject/notify 是 [callbacks.fireWith](http://www.cnblogs.com/snandy/archive/2012/11/15/2770237.html#fireWith)，执行回调函数；
- resolveWith/rejectWith/notifyWith 是 [callbacks.fireWith](http://www.cnblogs.com/snandy/archive/2012/11/15/2770237.html#fireWith) 队列方法引用。

最后合并promise到Deferred。

```plain
promise.promise( deferred );
jQuery.extend( obj, promise );
```

所以最终通过工厂方法Deferred构建的异步对象带的所有的方法了，return内部的deferred对象了。

### 测试Deferred代码

```javascript
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<script src="http://code.jquery.com/jquery-latest.js"></script>
<title></title>
</head>
<body>

<button>测试Deferred</button>

<script type="text/javascript">
      
    function Deferred(){
      //内部deferred对象
      var deferred = {};

      //定义的基本接口
      //Callbacks(once memory)的用法，就是只执行一次，并且保持以前的值
      // 每个元组分别包含一些与当前deferred相关的信息: 
      // 分别是：触发回调函数列表执行(函数名)，添加回调函数（函数名），回调函数列表（jQuery.Callbacks对象），deferred最终状态（第三组数据除外）
      // 总体而言，三个元组会有对应的三个callbacklist对应于doneList, failList, processList
      var tuples = [
        ["resolve", "done", jQuery.Callbacks("once memory"), "resolved"],
        ["reject", "fail", jQuery.Callbacks("once memory"), "rejected"],
        ["notify", "progress", jQuery.Callbacks("memory")]
      ];

      //deferred的状态，三种：pending(初始状态), resolved(解决状态), rejected(拒绝状态)
      //其实就是tuples最后定义的
      var state = "pending";

      //内部promise对象,作用：
      //1：通过promise.promise( deferred );混入到deferred中使用
      //2：可以生成一个受限的deferred对象，
      //   不在拥有resolve(With), reject(With), notify(With)这些能改变deferred对象状态并且执行callbacklist的方法了
      //   换句话只能读，不能改变了
      //扩展
      //  done fail pipe process 
      var promise = {
        state: function() {},
        always: function() {},
        then: function() {},
        promise: function(obj) {
          return obj != null ? jQuery.extend(obj, promise) : promise;
        }
      }

      //管道接口,API别名
      promise.pipe = promise.then;

      //遍历tuples
      //把定义的接口混入到deferred中
      jQuery.each(tuples, function(i, tuple) {
        var list = tuple[2],
          stateString = tuple[3];

          // 给上面的promise对象添加done，fail，process方法
          // 分别引用三个不同 jQuery.Callbacks("once memory")对象的add方法，在初始化就构建成了对象
          // 向各自的回调函数列表list（各自闭包中）中添加回调函数，互不干扰
          // promise = {
          //    done:
          //    fail:
          //    process
          // }
          promise[tuple[1]] = list.add;

        if (stateString) {
          list.add(function() {
            state = stateString;
          }, tuples[i ^ 1][2].disable, tuples[2][2].lock);
        }
        deferred[tuple[0]] = function() {
          deferred[tuple[0] + "With"](this === deferred ? promise : this, arguments);
          return this;
        };
        deferred[tuple[0] + "With"] = list.fireWith;
      });
      //混入方法
      promise.promise(deferred);

      return deferred;
    }
  $("button").on("click", function() {
    var dtd = Deferred();
    // 给deferred注册一个成功后的回调通知
    dtd.done(function() {
       $('body').append('<li>Deferred成功</li>')
    })
    // 开始执行一段代码
    setTimeout(function() {
      dtd.resolve(); // 改变deferred对象的执行状态
    }, 500);
  })
</script>
</body>
</html>
```

## Deferred源码剖析(下)

在上一节中构建了deferred对象，实现了done/fail/process和resolve/reject/notify等方法，但是最重要的then,pipe管道接口我们还没有实现，我们考虑下：

```javascript
var dfd = $.Deferred()
dfd.then(function(preVale) {
  return 2 * preVale   //4
}).then(function(preVale) {
  return 3 * preVale   //12
})
dfd.resolve(2)
```

then就是pipe，我们可以想象是一个管道，可以对回调模式使用瀑布模型。如案例所示，下一个回调都能取到上一个回调的值，这样一直可以叠加往后传递。

不难看出管道的风格就是链式的操作，每一个链上的结果都会反馈后下一个链，那么这个链式是不是传统的返回自身这个对象this呢？

常规的办法通过数组处理：右侧代码所示。

```javascript
function aDeferred(）{
   //代码右侧代码
}
```

这样的结构当然是很简陋的，这里我们最终有一个本质的问题没有解决，jQuery中的then的返回还有可能是另一个新的异步模型对象,如ajax，因此还能实现done，fail,always,then等方法。所以采用简陋的数组的方式保存状态是很肤浅的了。

这时候jQuery采取了对象保存处理：

```plain
我们可以把每一次的then操作，当做是创建一个新的deferred对象，那么每一个对象都够保存自己的状态与各自的处理方法。通过一个办法把所有的对象操作都串联起来，这就是then或者pipe管道设计的核心思路了。
```

看jQuery的**then**结构：

```javascript
then: function( /* fnDone, fnFail, fnProgress */ ) {
         var fns = arguments;
         return jQuery.Deferred(function(newDefer) {
                   jQuery.each(tuples, function(i, tuple) {
                            deferred[tuple[1]](function() {
                         // deferred[ done | fail | progress ]                   
                    });
               });
         }).promise()
```

其实在内部创建了一个新的Deferred对象，不过这里的不同是通过传递一个回调函数，参数是newDefer，其实Deferred内部就是为了改变下上下文this为deferred，然后传递deferred给这个回调函数了，所以newDefer就指向内部的deferred对象了。

那么对象之间如何关联？

```javascript
jQuery.each(tuples, function(i, tuple) {
  //取出参数
  var fn = jQuery.isFunction(fns[i]) && fns[i];
  // deferred[ done | fail | progress ] for forwarding actions to newDefer
  // 添加done fail progress的处理方法
  // 针对延时对象直接做了处理
  deferred[tuple[1]](function() {
    var returned = fn && fn.apply(this, arguments);
    if (returned && jQuery.isFunction(returned.promise)) {
      returned.promise()
        .done(newDefer.resolve)
        .fail(newDefer.reject)
        .progress(newDefer.notify);
    } else {
      newDefer[tuple[0] + "With"](this === promise ? newDefer.promise() : this, fn ? [returned] : arguments);
    }
});
```

把then的方法通过：

```javascript
deferred.done
deferred.fail
deferred.progress
```

加入到上一个对象的各自的执行队列中保存了。这样就实现了不同对象之间的关联调用。

同样如果then返回的是一个promise对象（ajax）的时候：

```javascript
if (returned && jQuery.isFunction(returned.promise)) {
  returned.promise()
    .done(newDefer.resolve)
    .fail(newDefer.reject)
    .progress(newDefer.notify);
```

也可以直接处理了。

### 模拟的代码测试

```plain
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<script src="http://code.jquery.com/jquery-latest.js"></script>
<title></title>
</head>
<body>

<button>模拟的代码测试</button>

<script type="text/javascript">
  
  //使用$.Deferred
  var dfd = $.Deferred()
  dfd.then(function(preVale) {
    return 2 * preVale; 
  }).then(function(preVale) {
    return 3 * preVale 
  }).then(function(preVale) {
    $('body').append('<li>使用$.Deferred代码结果:'+ preVale +'</li>')
  })

  dfd.resolve(2)

  //简单模拟
  function aDeferred() {
    var arr = [];
    return {
      then: function(fn) {
        arr.push(fn)
        return this;
      },
      resolve: function(args) {
        var returned;
        arr.forEach(function(fn, i) {
          var o = returned || args;
          returned = fn(o)
        })
      }
    }
  }
$("button").on("click", function() {
  var d = aDeferred();
  d.then(function(preVale) {
    return 2 * preVale //4
  }).then(function(preVale) {
    return 3 * preVale //4
  }).then(function(preVale) {
    $('body').append('<li>模拟代码结果:'+ preVale +'</li>')
  });
  d.resolve(2)
});
</script>
</body>
</html>
```

### when方法的设计

when也是一个非常有用的方法，常用于合并多个异步操作：

```plain
$.when(d1,d2,d3,d4......).done(function(v1, v2,v3...) {
    //等待所有异步加载完毕后执行
});
```

用法很简单，把所有的异步丢到when中，when会处理所有的结果。当然d1,d2,d3都是有规范的，都是通过Deferred产生的。

如果向 `jQuery.when()` 传入延迟对象，那么会返回它的 Promise 对象(延迟方法的一个子集)。可以继续绑定 Promise 对象的其它方法，例如， `defered.then` 。当延迟对象已经被解决（resolved）或被拒绝(rejected）（通常是由创建延迟对象的最初代码执行的），那么就会调用适当的回调函数。例如，由 `jQuery.ajax()` 返回的 jqXHR 对象是一个延迟对象，可以向下面这样使用：

```javascript
$.when($.ajax("test.aspx")).then(function(data, textStatus, jqXHR) {
  alert(jqXHR.status); // alerts 200
});
```

我们通过模拟的代码，可以很简单的分析整个流程：

1. 传递了多个异步对象，然后遍历每个异步对象给每一个对象绑定done、fail、progess方法，无非就是监听每一个异步的状态（成功，失败），如果是完成了自然会激活done方法。
2. updateFunc是监听方法，通过判断异步对象执行的次数来决定是不是已经完成了所有的处理或者是失败处理
3. 因为`when也要形成异步操作，`比如when().done()，`所以内部必须新建一个`jQuery.Deferred()对象，用来给后面链式调用。
4. 此刻监听所有异步对象(d1,d2…)的updateFunc的处理都完毕了，会给一个正确的通知给when后面的done方法，因为done是通过第三步jQuery.Deferred()创建的，所以此时就需要发送消息到这个上面，即：

```plain
deferred.resolveWith(contexts, values);
```

5. 内部的jQuery.Deferred()因为外部绑定了when().done(),所以done自然就收到了updateFunc给的消息了，可以继续之后的操作了。

所以整个执行流程就是这样简单，我们通过右边最简单的模拟出这个效果。

整个when的设计其实最终还是依赖了jQuery.Deferred内部处理的机制，一层套一层。当然jQuery的异步设计逻辑也确实很复杂，需要思维跳转很活跃，某一个时间在这里，下一个片段又要另一个地方去了，不是按照同步代码这样执行的。需要大家有一定的空间跳跃力了。

### when代码测试

```javascript
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<script src="http://code.jquery.com/jquery-latest.js"></script>
<script src="http://img.mukewang.com/down/541f6ff70001a0a500000000.js" type="text/javascript"></script>
<title></title>
</head>
<body>

<button>$.when代码测试</button>
<button>when模拟的代码测试</button>

<script type="text/javascript">

$('button').eq(0).click(function() {
  var d1 = new $.Deferred();
  var d2 = new $.Deferred();

  setTimeout(function(){
    d1.resolve("$.when代码测试Fish");
  },500)

  setTimeout(function(){
    d2.resolve("$.when代码测试Pizza");
  },1000)

$.when(d1, d2).done(function(v1, v2) {
  show(v1); // "Fish"
  show(v2); // "Pizza"
});  
})
ul
$('button').eq(1).click(function() {

  var d1 = new $.Deferred();
  var d2 = new $.Deferred();

  setTimeout(function() {
    d1.resolve("when模拟:Fish");
  }, 500)

  setTimeout(function() {
    d2.resolve("when模拟:Pizza");
  }, 1000)

  function when(d1, d2) {
    var i = 0,
      resolveValues = [].slice.call(arguments),
      length = resolveValues.length;
    var len = length;
    //收集resolve值
    var values = [];
    var deferred = jQuery.Deferred();

    function updateFunc(value) {
      values.push(value);
      if (len === 1) {
        deferred.resolveWith('contexts', values);
      }
      len--
    }
    for (; i < length; i++) {
      resolveValues[i].done(updateFunc)
    }
    return deferred;
  }
  when(d1, d2).done(function(v1, v2) {
    show(v1); // "Fish"
    show(v2); // "Pizza"
  });
})
</script> 
</body>
</html>
```
