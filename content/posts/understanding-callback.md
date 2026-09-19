---
title: "理解回调函数"
date: 2016-12-10
categories: ["前端"]
tags: ["前端"]
url: "/理解回调函数.html"
math: true
---

主要讲解回调函数在jQuery中的使用技巧与实现原理，概念上的东西看似简单，但是在实际运用中要做到灵活自如却也不是那么容易的事，而且对于部分开发者来说它仍然是一个谜。在阅读本文之后你能深入理解这个“回调函数”。

函数是第一类对象，这是javascript中的一个重要的概念。意味着函数可以像对象一样按照第一类管理被使用，所以在javaScript中的函数：

**☑ **  能“存储”在变量中

** ☑**   能作为函数的实参被传递

**☑ **  能在函数中被创建

** ☑**   能从函数中返回

**百科里面是这么解释的：**

回调函数就是一个通过函数指针调用的函数。如果你把函数的指针（地址）作为参数传递给另一个函数，当这个指针调用它所指向的函数时，我们就说这是回调函数。回调函数不是由该函数的实现方直接调用，而是在特定的事件或条件发生时由另外的一方调用的，用于对该**事件**或**条件**进行响应。

因此从上面可以看出来，回调本质上是一种设计原则，并且jQuery的设计原则遵循了这个模式。

在后端的编程语言中，传统函数以参数形式输入数据，并且使用返回语句返回值。理论上，在函数结尾处有一个return返回语句，结构上就是：一个输入和一个输出。简单的理解函数本质上就**是输入和输出之间实现过程的映射**。

但是，当函数的实现过程非常漫长，你是选择等待函数完成处理，还是使用回调函数进行异步处理呢？这种情况下，使用回调函数变得至关重要，例如：AJAX请求。若是使用回调函数进行处理，代码就可以继续进行其他任务，而无需空等。实际开发中，经常在javascript中使用异步调用。

**jQuery中遍地都是回调的设计：**

**异步回调：**

事件句柄回调

```plain
$(document).ready(callback);
$(document).on(‘click’,callback)
```

Ajax异步请求成功失败回调

```plain
$.ajax({
  url: "aaron.html",
  context: document
}).done(function() { 
        //成功执行
}).fail(function() {
        //失败执行
);
```

动画执行完毕回调

```plain
$('#clickme').click(function() {
    $('#book').animate({
        opacity: 0.25,
        left: '+=50',
        height: 'toggle'
    }, 5000, function() {
        // Animation complete.
    });
});
```

以上都是jQuery的回调直接运用，运用基本都是将匿名函数作为参数传递给了另一个函数或方法。而且以上都有一个特点，执行的代码都是异步的。

**同步回调：**

当然回调不仅仅只是处理异步，一般同步(很耗时的任务)的场景下也经常用到回调，比如要求执行某些操作后执行回调函数。

一个同步(阻塞)中使用回调的例子，目的是在test1代码执行完成后执行回调callback

```plain
var test1 = function(callback) {
    //执行长时间操作
    callback();
}
test1(function() {
    //执行回调中的方法
});
```

**所以理解回调函数最重要的2点：**

1、一个回调函数作为参数传递给另一个函数是，我们仅仅传递了函数定义。我们并没有在参数中执行函数。我们并不传递像我们平时执行函数一样带有一对执行小括号()的函数

2、回调函数并不会马上被执行，它会在包含它的函数内的某个特定时间点被“回调”。

## 回调的灵活运用

我们经常会这样使用函数回调：

**☑**  事件触发通知

**☑**  资源加载通知

**☑**  定时器延时

**☑**  ajax、动画通知等等。

以上都是很单一的事件监听回调的处理方式，但是jQuery把回调函数的用法设计成一个更高的抽像，用于解耦与分离变化。

如何理解这个设计？我们看下面的例子。

**例子一：**

jQuery针对Dom的处理提供了append、prepend、before、after等方法的处理，这几个方法的特征：

1、参数的传递可以是HTML字符串、DOM元素、元素数组或者jQuery对象

2、为了优化性能针对节点的处理需要生成文档碎片

可见几个方法都是需要实现这2个特性的，那么我们应该如何处理？

**高层接口：**

```javascript
before: function() {
    return this.domManip(arguments, function(elem) {
        if (this.parentNode) {
            this.parentNode.insertBefore(elem, this);
        }
    });
},

after: function() {
    return this.domManip(arguments, function(elem) {
        if (this.parentNode) {
            this.parentNode.insertBefore(elem, this.nextSibling);
        }
    });
},
```

**底层实现：**

```javascript
domManip: function(args, callback) {
    // Flatten any nested arrays
    args = concat.apply([], args);
    // We can't cloneNode fragments that contain checked, in WebKit
    if (isFunction ||
        //多参数处理
        self.domManip(args, callback);
    }

    if (l) {
        //生成文档碎片
        fragment = jQuery.buildFragment(args, this[0].ownerDocument, false, this);
        callback.call(this[i], node, i);
    }
    return this;
}
```

我们观察下jQuery的实现，通过抽象出一个domManip方法，然后在这个方法中处理共性，合并多个参数的处理与生成文档碎片的处理，然后最终把结果通过回调函数返回给每一个调用者。

**例子二：**

在很多时候需要控制一系列的函数顺序执行。那么一般就需要一个队列函数来处理这个问题。

我们看一段代码：

```plain
function Ulson(List, callback) {
    setTimeout(function() {
        var task;
        if (task = List.shift()) {
            task(); //执行函数
        }
        if (List.length > 0) { //递归分解
            arguments.callee(List)
        } else {
            callback()
        }
    }, 25)
}

//调用
Ulson([
    function() {
        alert('a')
    },
    function() {
        alert('b')
    },
    function() {
        alert('c')
    }
], function() {
    alert('callback')
})

// 分别弹出 ‘a’ , ‘b’ ,'c',’callback
```

传入一组函数参数，靠递归解析，分个执行，其实就是靠setTimeout可以把函数加入到队列末尾才执行的原理，这样的写法就有点就事论事了，聚合对象完全是一个整体，无法再次细分出来，所以我们需要一种方案，用来管理分离每一个独立的对象。

**我们换成jQuery提供的方式:**

```plain
var callbacks = $.Callbacks();
callbacks.add(function() {
    alert('a');
})
callbacks.add(function() {
    alert('b');
})
callbacks.fire(); //输出结果: 'a' 'b'
```

是不是便捷很多了，代码又很清晰，所以Callbacks它是一个多用途的回调函数列表对象，提供了一种强大的方法来管理回调函数队列。

那么我们使用回调函数，总的来说**弱化耦合**，让调用者与被调用者分开，调用者不关心谁是被调用者，所有它需知道的，只是存在一个具有某种特定原型、某些限制条件的被调用函数。

## 理解观察者模式

讲解jQuery回调对象之前，我们有必要先理解其背后的设计思想 - “观察者模式”。

观察者模式 (pub/sub) 的背后，总的想法是在应用程序中增强松耦合性。并非是在其它对象的方法上的单个对象调用。一个对象作为特定任务或是另一对象的活动的观察者，并且在这个任务或活动发生时，通知观察者。观察者也被叫作订阅者（Subscriber），它指向被观察的对象，既被观察者（Publisher 或 subject)。当事件发生时，被观察者（Publisher）就会通知观察者（subscriber）。

**观察者的使用场合**

观察者的使用场合就是：**当一个对象的改变需要同时改变其它对象，并且它不知道具体有多少对象需要改变的时候，就应该考虑使用观察者模式**。先看官网的demo这个例子，涉及到了 add 与 fire方法，熟悉设计模式的童鞋呢，一眼就能看出，其实又是基于发布订阅（Publish/Subscribe）的观察者模式的设计。

作为 $.Callbacks() 的创建组件的一个演示，只使用回调函数列表，就可以实现 Pub/Sub 系统，将 $.Callbacks 作为一个队列。

**我们来模拟常规下最简单的实现：**

JS里对观察者模式的实现是通过回调来实现的，我们来先定义一个Observable对象，其内部包含了2个方法：订阅add方法与发布fire方法，如下代码：

```javascript
var Observable = {
  callbacks: [],
  add: function(fn) {
    this.callbacks.push(fn);
  },
  fire: function() {
    this.callbacks.forEach(function(fn) {
      fn();
    })
  }
}
```

使用add开始订阅：

```plain
Observable.add(function() {
  alert(1)
})
Observable.add(function() {
  alert(2)
})
```

使用fire开始发布：

```plain
Observable.fire(); // 1, 2
```

**设计的原理：**

开始构建一个存放回调的数组，如`this.callbacks= []`添加回调时，将回调push进this.callbacks，执行则遍历this.callbacks执行回调，也弹出1跟2了。当然这只是简洁的设计，便于理解，整体来说设计的思路代码都是挺简单的，那么我们从简单的设计深度挖掘下这种模式的优势。

注意：如果没有做过复杂交互设计，或者大型应用的开发者，可能一开始无法理解这模式的好处，就简单的设计而言用模式来处理问题，有点把简单的问题复杂化。我们不是为了使用模式而使用的。

**组件开发为了保证组件可以在不同的项目中都适用，其必须是对其常用功能抽象出来加以实现，绝不会包含具体的业务逻辑而某一特定的项目使用者在其业务场景中使用组件时不可避免的要加入不同场景的业务逻辑。**

## 模式的实际运用

在进行组件开发中，为了保证组件可以在不同的类似项目场景中都能适用，那么就必须是对其常用功能抽象出来加以实现。

我们来看看具体的实际用处：

假设一段ajax的请求，成功后通过done返回结果数据：

```javascript
$.ajax({
  url: "test.html",
  context: document.body
}).done(function(data) {
  //data数据的处理
  $('aaron1').html(data.a)
  $('aaron2').html(data.b)
  $('aaron3').html(data.c)
  //其余处理
});
```

咋一看好像都挺好，没什么问题，但是仔细观察我们会发现所有的逻辑是不是都写在done方法里面，这样确实是无可厚非的，但是问题就是逻辑太复杂了。Done里面有数据处理、html渲染、还可能有其它不同场景的业务逻辑。这样如果是换做不同的人去维护代码，增加功能就会显得很混乱而且没有扩展性。那么观察者模式能很好的解决了这个的问题。

我们优化下代码:

```plain
$.ajax({
  url: "test.html",
  context: document.body
}).done(function(data) {
    pocessData()
    pocessHtml()
    pocessOther()
  }

  function pocessData() {
    //处理数据
  }

  function pocessHtml() {
    $('aaron1').html(data.a)
    $('aaron2').html(data.b)
    $('aaron3').html(data.c)
  }

  function pocessOther() {
    //处理其他逻辑
  }
```

这种方式的好处是，分离出各种的业务函数，从而降低了代码之间的耦合度，但是这样代码写法几乎就是“就事论事”的处理，达不到**抽象复用**。

那么我们用之前的观察者模式加工一下上面的代码：（这只是伪代码，用于理解）

```plain
Observable.add(function() {
  //pocessData
})

Observable.add(function() {
  $('aaron1').html(data.a)
  $('aaron2').html(data.b)
  $('aaron3').html(data.c)
})

Observable.add(function() {
  //pocessOther
})

$.ajax({
  url: "test.html",
  context: document.body
}).done(function(data) {
  Observable.fire(data)
})
```

设计该模式背后的主要动力是促进形成松散耦合。在这种模式中，并不是一个对象调用另一个对象的方法，而是一个对象订阅另一个对象的特定活动并在状态改变后获得通知。订阅者也称为观察者，而被观察的对象称为发布者或主题。当发生了一个重要的事件时，发布者将会通知（调用）所有订阅者并且可能经常以事件对象的形式传递消息。

总的来说，观察者模式所做的工作就是在解耦，让耦合的双方都依赖于抽象，而不是依赖于具体。从而使得各自的变化都不会影响到另一边的变化。

```javascript
var Observable = {
  callbacks: [],
  add: function(fn) {
    this.callbacks.push(fn);
  },
  fire: function(data) {
      this.callbacks.forEach(
          function(fn) {fn(data);})
  }
}
function ajax(arg){
  setTimeout(function(){
    arg.successful(arg.data+ ',返回获取到后台的数据')
  },1000)
}

//使用add开始订阅：
Observable.add(function(data) {
  show('Action_one: ' + data)
})
Observable.add(function(data) {
  show('Action_two: ')
})

//一段ajax请求，成功后处理
ajax({
  data:'Hello',
  successful:function(data){
    Observable.fire(data); //触发动作
  }
})
```

## jQuery回调对象

jQuery.Callbacks一般开发者接触的很少，虽然jQuery向开发者提供了外部接口调用，但是$.Callbacks()模块的开发目的是为了给内部$.ajax() 和 $.Deferred()模块提供统一的基本功能组件。它可以用来作为类似基础定义的新组件的功能。

jQuery.Callbacks是jquery在1.7版本之后加入的，是从1.6版中的_Deferred对象中抽离的，主要用来进行函数队列的add、remove、fire、lock等操作，并提供once、memory、unique、stopOnFalse四个option进行一些特殊的控制。

这个函数常见的应用场景是事件触发机制，也就是设计模式中的观察者模式的发布、订阅机制，目前Callbacks对象用于queue、ajax、Deferred对象中，本小节主要是一些简单的例子去理解的使用。

我们看官网提供的demo：

```plain
function fn1(value) {
  console.log(value);
}

function fn2(value) {
  fn1("fn2 says: " + value);
  return false;
}
```

可以将上述两个方法作为回调函数，并添加到 $.Callbacks 列表中，并按下面的顺序调用它们:

```javascript
var callbacks = $.Callbacks();
callbacks.add(fn1);
// outputs: foo!
callbacks.fire("foo!");
callbacks.add(fn2);
// outputs: bar!, fn2 says: bar!
callbacks.fire("bar!")
```

这样做的结果是，当构造复杂的回调函数列表时，将会变更很简单。可以根据需要，很方面的就可以向这些回调函数中传入所需的参数。

上面的例子中，我们使用了 $.Callbacks() 的两个方法: .add() 和 .fire()。 .add() 和 .fire() .add() 支持添加新的回调列表, 而.fire() 提供了一种用于处理在同一列表中的回调方法的途径。

另一种方法是$.Callbacks 的.remove()方法，用于从回调列表中删除一个特定的回调。下面是.remove()使用的一个例子:

```plain
var callbacks = $.Callbacks();
callbacks.add( fn1 );
// outputs: foo!
callbacks.fire( "foo!" );
callbacks.add( fn2 );
// outputs: bar!, fn2 says: bar!
callbacks.fire( "bar!" );
callbacks.remove( fn2 );
// only outputs foobar, as fn2 has been removed.
callbacks.fire( "foobar" );
```

这个运用内部就是观察者模式的一种设计实现，只是相对比较复杂。我们看看jQuery的回调函数到底为哪些模块服务？

异步队列模块：

```plain
Deferred: function(func) {
  var tuples = [
    // action, add listener, listener list, final state
    ["resolve", "done", jQuery.Callbacks("once memory"), "resolved"],
    ["reject", "fail", jQuery.Callbacks("once memory"), "rejected"],
    ["notify", "progress", jQuery.Callbacks("memory")]
  ]，………….
```

队列模块

```plain
_queueHooks: function(elem, type) {
  var key = type + "queueHooks";
  return data_priv.get(elem, key) || data_priv.access(elem, key, {
    empty: jQuery.Callbacks("once memory").add(function() {
      data_priv.remove(elem, [type + "queue", key]);
    })
  });
}
```

Ajax模块

```plain
ajax: function(url, options) {
  //省略代码
  deferred = jQuery.Deferred(),
  completeDeferred = jQuery.Callbacks("once memory")
    ..............
}
```

不难发现jQuery.Callbacks还提供“once memory”等参数用来处理：

☑  once: 确保这个回调列表只执行（ .fire() ）一次(像一个递延 Deferred)。

☑  memory: 保持以前的值，将添加到这个列表的后面的最新的值立即执行调用任何回调 (像一个递延 Deferred)。

☑  unique: 确保一次只能添加一个回调(所以在列表中没有重复的回调)。

☑  stopOnFalse: 当一个回调返回false 时中断调用。

```javascript
var callbacks = $.Callbacks('once');

callbacks.add(function() {
  alert('a');
})

callbacks.add(function() {
  alert('b');
})

callbacks.fire(); //输出结果: 'a' 'b'
callbacks.fire(); //未执行
```

once的作用是使callback队列只执行一次。

最后，我们大概知道这个是干嘛用的了，可以开始上正菜了。

## jQuery回调模块结构

整个$.Callbacks的源码很少，它是一个工厂函数，使用函数调用（非new，它不是一个类）创建对象，它有一个可选参数flags用来设置回调函数的行为，对外的接口也就是self的返回。

jQuery.Callbacks()的API列表如下：

```javascript
callbacks.add()        ：回调列表中添加一个回调或回调的集合。
callbacks.disable()    ：禁用回调列表中的回调。
callbacks.disabled()   ：确定回调列表是否已被禁用。 
callbacks.empty()      ：从列表中删除所有的回调。
callbacks.fire()       ：用给定的参数调用所有的回调。
callbacks.fired()      ：访问给定的上下文和参数列表中的所有回调。 
callbacks.fireWith()   ：访问给定的上下文和参数列表中的所有回调。
callbacks.has()        ：确定列表中是否提供一个回调。
callbacks.lock()       ：锁定当前状态的回调列表。
callbacks.locked()     ：确定回调列表是否已被锁定。
callbacks.remove()     ：从回调列表中的删除一个回调或回调集合。
```

源码结构：

```javascript
jQuery.Callbacks = function(options) {
    options = typeof options === "string" ?
        (optionsCache[options] || createOptions(options)) :
        jQuery.extend({}, options);
    //实现代码
    fire = function() {}
    self = {
        add: function() {},
        remove: function() {},
        has: function(fn) {},
        empty: function() {},
        disable: function() {},
        disabled: function() {},
        lock: function() {},
        locked: function() {},
        fireWith: function(context, args) {},
        fire: function() {},
        fired: function() {}
    };
    return self;
};
```

整个结构要分三部分：

☑   Options参数缓存

☑   内部fire触发器的设计

☑   外部

**参数的缓存设计**

Callbacks是可以是接受的字符串的组合传参数，可以使用空格分割，代码如下：

```plain
var opts = 'unique memory';
var object = {}
jQuery.each(opts.match(/\S+/g) || [], function(_, flag) {
  object[flag] = true;
});
```

这样的操作其实是不需要重复的，所以我们可以设计一个缓存池，用来储存重复的操作：

```plain
var optionsCache = {};
function createOptions(options) {
  var object = optionsCache[options] = {};
  jQuery.each(options.match(rnotwhite) || [], function(_, flag) {
    object[flag] = true;
  });
  return object;
}
```

所以我们传递参数的时候，如果参数是字符串，我们可以直接从optionsCache缓存中去查找：

```plain
options = typeof options === "string" ?
        ( optionsCache[ options ] || createOptions( options ) ) :
        jQuery.extend( {}, options );
```

**接口的设计：**

通过学习了观察者模式的思路，我们知道callback需要在内部维护着一个list的队列数组，用于保存订阅的对象数据。同时也需要提供了add、remove、fire等订阅、发布、删除类似的接口。

那么我们代码是不是很简单是就是把订阅对象给push给内部list列表？

实现思路就是: 构建一个存放回调的数组，如`var list = []`，通过闭包使这条回调数组保持存在。添加回调时，将回调push进list，执行则遍历list执行回调。

后面几节我们会通过简单的模拟实现去剖析设计的思路。

## 默认回调对象设计

不传入任何参数，调用add的时候将函数add到内部的list中，调用fire的时候顺序触发list中的回调函数：

```plain
function fn1(val) {
  console.log('fn1 says:' + val);
}

function fn2(val) {
  console.log('fn2 says ' + val);
}
var cbs = $.Callbacks();
cbs.add(fn1);
cbs.fire('foo');
console.log('........')
cbs.add(fn2);
cbs.fire('bar')
```

结果就是按照顺序叠加触发，如下列表：

```plain
fn1 says:foo 
………………………
fn1 says:bar 
fn2 says bar
```

这种就是最简单的处理了，可以直接模拟，代码如下：

```plain
function Callbacks() {
  var list = [];
  var self;
  self = {
    add: function(fn) {
      list.push(fn)
    },
    fire: function(args) {
      list.forEach(function(fn) {
        fn(args);
      })
    }
  }
  return self;
}
```

## once的设计

这一小节我们来讲一下once。

once的作用确保回调列表只执行（.fire()）一次(像一个递延 Deferred)，如下代码：

```plain
function fn1(val){
    console.log('fn1 says ' + val);
}
var cbs = $.Callbacks('once');
cbs.add(fn1);
cbs.fire('foo');
cbs.fire('foo');
```

结果你会发现cbs.fire(‘foo’)只执行了一次。

```plain
fn1 says foo  //只显示一次
```

once定义是很明确的，确保这个回调列表只执行（ .fire() ）一次(像一个递延 Deferred)，所以针对这种once的处理可以有多种不同的途径实现。

1、add的时候抛弃

2、在fire的时候抛弃多个。

但是jQuery是在执行第一个fire的时候直接给清空list列表了，然后在add的地方给判断下list是否存在，从而达到这样的处理。

```plain
function Callbacks(options) {
  var list = [];
  var self;
  self = {
    add: function(fn) {
      list.push(fn)
    },
    fire: function(args) {
      if (list) {
        list.forEach(function(fn) {
          fn(args);
        })
        if (options === 'once') {
          list = undefined;
        }
      }
    }
  }
  return self;
}
```

在fire之后，判断参数是否为once，直接把list给清理掉，所以之后的所有fire都被抛弃掉了，而从达到了once的效果。

**jQuery.Callbacks的处理**

在fire中调用了 self.disable(); 方法

```plain
// 禁用回调列表中的回调。
disable: function() {
    list = stack = memory = undefined;
    return this;
},
```

## memory的设计

memory：保持以前的值，将添加到这个列表的后面的最新的值立即执行调用任何回调 (像一个递延 Deferred)。

回调函数是从异步队列Deferred分离出来的，所以很多的接口设计都是为了契合Deferred接口，memory用的很多，这个缓存的设计这里提及一下

主要是用来实现deferred的异步收集与pipe管道风格的数据传递的，具体在Deferred有详解，这里大概了解下作用范围。

memory这个有点不好理解，我们还是通过列子说明下，看下面的代码：

```plain
var cbs = Callbacks('once');
cbs.add(fn1);
cbs.fire('foo');
cbs.fire('foo');

function fn1(val) {
  console.log('fn1 says ' + val);
}
function fn2(val) {
  console.log('fn2 says ' + val);
}
function fn3(val) {
  console.log('fn3 says ' + val);
}

var cbs = $.Callbacks('memory');
cbs.add(fn1);
cbs.fire('foo');

console.log('..........')

cbs.add(fn2);
cbs.fire('bar');

console.log('..........')
cbs.add(fn3);
cbs.fire('aaron');
```

结果可以看出，我们在执行cbs.add(fn2);的时候，此时除了把fn2添加到了回调队列之外而且还立刻执行了这个方法，唯一的区别就是，参数是用的之前的。所以解释就叫“**保持以前的值**”。

```plain
fn1 says foo 
.......... 
fn2 says foo 
fn1 says bar 
fn2 says bar 
.......... 
fn3 says bar 
fn1 says aaron 
fn2 says aaron 
fn3 says aaron
```

所以这个`memory`设计需要解决的问题就是：

1：如何取到上一个参数

2：add后如何执行

看看我们实现的代码：

```javascript
function Callbacks(options) {
  var list = [];
  var self;
  var firingStart;
  var memory;

  function _fire(data) {
    memory = options === 'memory' && data;
    firingIndex = firingStart || 0;
    firingStart = 0;
    firingLength = list.length;
    for (; list && firingIndex < firingLength; firingIndex++) {
      list[firingIndex](data)
    }
  }

  self = {
    add: function(fn) {
      var start = list.length;
      list.push(fn)
      if (memory) {
        firingStart = start; //获取最后一值
        _fire(memory);
      }
    },
   fire: function(args) {
      if (list) {
        _fire(args)
      }
    }
  }
  return self;
}
```

首先add之后要能触发fire的动作，所以我们把fire作为内部的一个私有方法实现_fire，比较合逻辑，这样外部的fire只是一个门面方法的调用。

私有变量memory缓存这上一个参数的属性，我们靠firingStart用来定位最后通过add增加的回调数据的索引。在遍历的时候直接通过firingStart的起始索引定位，然后传递memory的参数，而且实现这种“保持以前的值”的设计。

## unique的设计

Unique：确保一次只能添加一个回调(所以在列表中没有重复的回调)

```plain
function fn1(val) {
  console.log('fn1 says ' + val);
}
var callbacks = $.Callbacks( "unique" );
callbacks.add( fn1 );
callbacks.add( fn1 ); // repeat addition
callbacks.add( fn1 );
callbacks.fire( "foo" );
```

结果：过滤了相同的add操作

```plain
fn1 says foo
```

过滤重复的比较简单，因为是数组的保存方式，我们可以在入口处通过indexOf判断即可

```plain
function Callbacks(options) {
  var list = [];
  var self;
  var firingStart;
  var memory;

  function _fire(data) {
    memory = options === 'memory' && data;
    firingIndex = firingStart || 0;
    firingStart = 0;
    firingLength = list.length;
    for (; list && firingIndex < firingLength; firingIndex++) {
      list[firingIndex](data)
    }
  }

  self = {
    add: function(fn) {
      var start = list.length;
      if (options == 'unique') {
        if (-1 === list.indexOf(fn)) {
          list.push(fn)
        }
      } else {
        list.push(fn)
      }
      if (memory) {
        firingStart = start; //获取最后一值
        _fire(memory);
      }
    },
    fire: function(args) {
      if (list) {
        _fire(args)
      }
    }
  }
  return self;
}
```

## stopOnFalse

stopOnFalse: 当一个回调返回false 时中断调用

```plain
function fn1(value) {
  console.log(value);
  return false;
}

function fn2(value) {
  fn1("fn2 says: " + value);
  return false;
}

var callbacks = $.Callbacks("stopOnFalse");
callbacks.add(fn1);
callbacks.fire("foo");

callbacks.add(fn2);
callbacks.fire("bar");
```

结果虽然fn1被添加到了回调列表，但是因为fn1返回了false，那么意思之后的回调都不会被调用了。如果还有fn3，在f2上返回false，fn3也将不会被调用。

```plain
foo
bar
```

这个设计我们只要控制好函数返回的处理的布尔值，通过这个值用来判断是否需要下一个遍历

```plain
if (list[firingIndex](data) === false && options === 'stopOnFalse') {
  break;
}
```

源码可以如下：

```plain
function Callbacks(options) {
  var list = [];
  var self;
  var firingStart;
  var memory;

  function _fire(data) {
    memory = options === 'memory' && data;
    firingIndex =
      firingStart || 0;
    firingStart = 0;
    firingLength = list.length;
    for (; list && firingIndex < firingLength; firingIndex++) {
      if (list[firingIndex](data) === false && options === 'stopOnFalse') {
        break;
      }
    }
  }

  self = {
    add: function(fn) {
      var start = list.length;
      if (options == 'unique') {
        if (-1 === list.indexOf(fn)) {
          list.push(fn)
        }
      } else {
        list.push(fn)
      }
      if (memory) {
        firingStart = start; //获取最后一值
        _fire(memory);
      }
    },
    fire: function(args) {
      if (list) {
        _fire(args)
      }
    }
  }
  return self;
}
```

以上是几种单独的处理情况的用法，我们可以看到jQuery都是组合使用的，最常见的就是

jQuery.Callbacks(“once memory”)的组合了，其实以上的思路都讲解过了，无非就是组合起来的时候要考虑一些判断了。
