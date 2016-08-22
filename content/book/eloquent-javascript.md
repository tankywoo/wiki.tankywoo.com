---
title: "JavaScript编程精解"
date: 2016-06-25 21:35
updated: 2016-07-17 16:25
tag: web, javascript
---

[TOC]

## JavaScript基础部分

数字: JavaScript 使用固定长度为64位的位序列来存储数字值。

几个特殊的数字：

* `Infinity`: 正无穷大
* `-Infinity`: 负无穷大
* `NaN`: 非数值，表示无意义的值

`typeof` 一元运算符，获取给定值的具体类型：

```javascript
> typeof "abcd"
'string'
```

布尔值：`true` / `false`

逻辑运算符：`&&` / `||` / `!`

未定义值 (两者基本等价)

* `null`
* `undefined`

JavaScript对于不同类型的运算或比较会进行自动类型转换。对于比较，可以使用严格比较：`===` 和 `!==`

`var`定义变量，可以同时定义多个变量，并用逗号分隔：

	var a = 1, b = 2;

几个函数：

* `alert`
* `confirm`
* `prompt`
* `isNaN`
* `Number` 强制转换为数值
* `console.log` 适合调试用

if语句：

	if (...)
	  ...;
	else if (...)
	  ...;
	else
	  ...;

while语句：

	while (...) {
	  ...;
	}

do..while语句：

	do {
	  ...;
	} while (...);  // 注意有分号

for循环：

	for (var i = 0; i <= 100; i++) {
	  if (i == 5)
	    break;  // break语句
	}

switch语句：

	switch (...) {
	  case condition1:
	    ...;
	    break
	  case condition2:
	    ...;
	    break
	  ...
	  default:
	    ...;
	    break
	}

对于switch, 每一个条件后加上`break`是个好习惯，否则比如匹配到condition1后，后面的语句都会执行，不管是否匹配的。如果没有任何匹配，则会跳到`default`标签。

注视：

* `//` 适合单行注释
* `/* .... */` 适合块注释

经验：

* 变量声明/定义都以`var`开头
* 语句都以`分号`结尾
* 缩进使用`2个空格`

函数定义的两种方式：

方式一，直接定义匿名函数，赋值给一个变量：

	var square = function(x) {
	  return x * x;
	};  // 分号结尾

	console.log(square(10));

方式二，直接做**函数声明**：

	console.log(square(10));
	
	function square(x) {
	  return x * x;
	}  // 无分号

这种方式不需要遵守从上而下的定义方式。

注：

* 注意函数中变量作用域，只有在函数内部用`var`定义的变量才属于函数内
* 在JS中，只有函数能够创建新的作用域
* JS对传入函数的参数数量几乎没有任何限制。如果有参数定义但是没有传参，则这些变量为undefined

当函数被调用时，函数体内部会添加一个特殊变量`arguments`，指向一个包含所有传入传输的对象。

此对象有length属性，和数组比较类似，但是不包含数组的任何方法

数组：

	> var arr = [1,2,3,4];
	> typeof arr
	'object'

数组也是一种对象

属性：如Math.max，mystr.length; 可以通过点号`.`或方括号`[]`获取，后者的key可以是带有空格的

	> ['a', 'b', 'c'].length
	3

方法：如mystr.toUpperCase()

	> typeof 'abc'.toUpperCase
	'function'
	> 'ABc'.toLowerCase()
	'abc'

数组的几个方法：

* join
* push: 在末尾添加
* pop: 在末尾删除
* unshift: 在开头添加
* shift: 在开头删除
* indexOf: 从第一个元素向后搜索
* lastIndexOf: 从最后一个元素向前搜索
* concat: 拼接两个数组(类似于python中的extend)
* slice: 取其中一部分数组 (不清楚这个和直接arr[i1:i2]有什么区别?)
对象：

创建对象的方式之一是使用大括号：

	var desc = {
	  work: 'program',
	  'my name': 'tanky',
	  'other': function() {
		return 'hello world';
	  }
	}

	> typeof desc
	'object'
	> desc.other();
	'hello world'

JS中对象的属性/方法是`**引用**`方式。

* `in` 二元操作符，判断属性或方法是否在对象中
* `delete` 一元操作符，从对象中移除指定的属性

可以直接通过`=`给对象的属性/方法赋值，如果属性/方法不存在，则相当于新增属性，否则相当于修改属性。

对于对象，引用两个相同的对象和两个不同对象包含相同属性是一样的：

	> var obj1 = {'value': 10};
	> var obj2 = obj1;
	> var obj3 = {'value': 10};
	> obj1 == obj2;
	true
	> obj1 == obj3;
	false
	> obj1.value = 15;
	15
	> obj2.value
	15
	> obj3.value
	10

遍历对象，使用`for (var name in object)`方式：

	> for (var i in desc) {
		console.log('k: ' + i + ', v: ' + desc[i]);
	  }
	k: work, v: program
	k: my name, v: tanky
	k: other, v: function () {
	return 'hello world';
	}

字符串、数字、布尔等都不是对象，所以不能添加属性，添加不会报错，不过没什么作用。

Math对象：

* min: 求最小值
* max: 求最大值
* sqrt: 求平方根
* 三角函数sin, cos, tan ...
* random: 0-1之间的随机数
* floor: 向下取整
* ceil: 向上取整
* round: 四舍五入

全局对象 `window`：每一个全局变量作为一个属性，存储在全局对象中。在浏览器中，全局对象存储在window变量中。

	> var a = 100;
	> 'a' in window;
	true

数组的`forEach`方法：

	function square_arr(arr) {
	  var n_arr = [];
	  arr.forEach(function(x) {
		n_arr.push(x * x);
	  });
	  return n_arr;
	}

	console.log(square_arr([1,2,3,4]));  // [1, 4, 9, 16]

数组的`filter`方法用于过滤：

	// 过滤出所有的奇数
	var arr = [1, 2, 3, 4, 5];

	console.log(arr.filter(function(v) {
	  return v % 2;
	}));

数组的`map`方法用于对每一个元素分别调用函数，生成一个新的数组：

	// 和上面forEach效果一样，对数组进行求平方
	var arr = [1, 2, 3, 4, 5];

	console.log(arr.map(function(v) {
	  return v * v;
	}));

数组的`reduce`方法用于折叠数组，接收用于合并操作的函数以及初始值，如果初始值没写，则默认表示0；合并函数接收两个参数，即前一次和本次：

	// 数组所有元素求和
	var arr = [1, 2, 3, 4, 5];

	console.log(arr.reduce(function(pre, cur) {
	  return pre + cur;
	}));

函数的`apply`方法，接收一个数组或类数组的参数（所以可以把arguments传过去）

函数的`call`方法，接收一系列参数，和`apply`相比相当于把参数数组展开

函数的`bind`方法新生成一个函数，并把传递的参数当做上下文一起传过去。

参考：

* [What is the difference between call and apply?](http://stackoverflow.com/questions/1986896/what-is-the-difference-between-call-and-apply)
* [Javascript call() & apply() vs bind()?](http://stackoverflow.com/questions/15455009/javascript-call-apply-vs-bind)


与JSON相关的两个方法：

* `JSON.stringify`：输入javascript变量，返回JSON编码后的字符串
* `JSON.parse`：输入一个字符串，返回解码后的值

在调用object.method()时，对象中的一个特殊变量`this`会指向当前方法所属的对象。

原型(prototype)：原型是另一个对象，是对象的属性来源，当访问一个对象不包含的属性时，会从对象原型中搜索属性，接着是原型的原型...

JS对象原型的关系是一种树形结构，根部就是Object.prototype；

子对象可以继承父对象的属性。

原型是一层层继承下来，比如函数继承自原型Function.prototype，数组继承自Array.prototype。

通过`Object.getPrototypeOf()`返回一个对象的原型：

	function func() {
	};

	// true
	console.log(Object.getPrototypeOf(func) == Function.prototype);

通过`Object.create`利用一个特定的原型来创建对象。

	var protoObj = {
	  say: function() {
		console.log('hello');
	  }
	};

	var my_obj = Object.create(protoObj);
	// print 'hello'
	my_obj.say();

	// true
	console.log(Object.getPrototypeOf(my_obj) == protoObj);

构造函数：

(**这块内容有点绕，需额外再研究下**)

在JS中，调用函数之前添加一个关键字`new`则表示调用其构造函数；构造函数中包含了指向新对象的变量this。

通过关键字`new`创建的对象称之为构造函数的实例。

构造函数的名称一般以大写字母开头，便于与其它函数区分。

所有使用特定构造函数创建的对象，都会将构造函数的prototype属性作为其原型。

	function Rabbit(type) {
	  this.type = type;
	}

	var killerRabbit = new Rabbit("killer");
	var blackRabbit = new Rabbit("black");
	// black
	console.log(blackRabbit.type);

	Rabbit.prototype.speak = function(line) {
	  console.log("The " + this.type + " rabbit says '" + line + "'");
	};

	blackRabbit.speak("Hello...");

关于原型，有`可枚举(enumerable)`和`不可枚举(nonenumerable)`属性：

* 可枚举：我们创建并赋予对象的所有属性
* 不可枚举：Object.prototype中的标准属性

`in` 可以测试属性是否在对象中：

	var map = {'one': 1, 'two': 2}

	Object.prototype.nonsense = "hi";

	// one
	// two
	// nonsense  <-- nonsense也在
	for (var n in map)
	  console.log(n);

	// true
	console.log("nonsense" in map);
	// true
	console.log("toString" in map);

`Object.defineProperty`函数可以定义自己的不可枚举属性：

	var map = {'one': 1, 'two': 2}

	Object.defineProperty(Object.prototype, "hiddenNonsense",
						  {enumerable: false, value: "hi"});

	// one
	// two
	for (var n in map)
	  console.log(n);

	// true
	console.log("hiddenNonsense" in map);
	// "hi"
	console.log(map.hiddenNonsense);

`in`并不能判断属性是自身还是原型中继承的，可以通过`hasOwnProperty`方法来判断：

	// false
	console.log(map.hasOwnProperty('toString'));

`instanceof`二元运算符用于判断某个对象是否继承自指定的构造函数：

	function Func1(text) {
	  this.text = text;
	}

	function Func2 (text) {
	  Func1.call(this, text);
	}
	Func2.prototype = Object.create(Func1.prototype);  // 继承

	console.log(new Func2('a') instanceof Func2);  // true
	console.log(new Func2('a') instanceof Func1); // true
	console.log(new Func1('a') instanceof Func2); // false

调试相关：

启用严格模式：在文件或函数体顶部加上字符串`"use strict"`

	function func() {
	  "use strict"
	  ...
	}

> 我们必须遏制住随意修改代码进行调试的冲动，思考才是最重要的。

1. 有目的的在程序中使用console.log输出额外信息
2. 断点：浏览器一般可以直接设置断点，或者使用`debugger`语句

(chrome下打开开发者工具->Sources, 找到相应JS代码，点击行号增加断点, 具体可以参考[chrome js debugging](https://developer.chrome.com/devtools/docs/javascript-debugging))

异常：`try .. catch .. finally`，其中finally可选，catch 到的异常值会绑定到圆括号中的变量：

	function func(value) {
	  if (value == 5)
		throw new Error("value can't equel 5");
	}

	try {
	  func(5);
	} catch (error) {
	  console.log('error: ', error);
	} finally {
	  console.log('exit with clean task...');
	}

JS并未对选择性捕获异常提供良好的支持，要不捕获所有异常，要不什么都不捕获。只能靠额外来支持：

	function InputError(msg) {
	  this.message = msg;
	  this.stack = (new Error()).stack;
	}
	InputError.prototype = Object.create(Error.prototype);
	InputError.prototype.name = 'InputError';

	function func(value) {
	  if (value == 5)
		throw new InputError("value can't equel 5");
	}

	try {
	  func(5);
	} catch (error) {
	  // if (! (error instanceof InputError))
	  if (error instanceof InputError)
		console.log('input error: ', error);
	} finally {
	  console.log('exit with clean task...');
	}

最后就是实现断言这个工具函数了，JS自身是没有提供这个语句：

	function AssertionFailed(message) {
	  this.message = message;
	}
	AssertionFailed.prototype = Object.create(Error.prototype);

	function assert(test, message) {
	  if (!test)
		throw new AssertionFailed(message);
	}

## 浏览器中的JavaScript

HTML中某些字符的特殊标记方法，格式`& + 单词 + ;`，成为实体。如`&lt;`表示小于号，`&gt;`表示大于号等。

文档对象模型(DOM, Document Object Model)

document.documentElement 根节点

每个DOM节点对象都包含`nodeType`属性，一个表示节点类型的数字代码，如：

* document.ELEMENT_NODE (1)
* document.TEXT_NODE (3)
* document.COMMENT_NODE (8)

通过树结构访问节点:

* parentNode
* childNodes (注意因为子节点一般会有多个，所以是Nodes)
* firstChild
* lastChild
* previousSibling
* nextSibling

因为`childNodes`是一个包含多个子节点的类数组对象，有`length`属性，所以可以循环访问：

```javascript
var node = document.body;
for (var i = 0; i < node.childNodes.length; i++) {
  console.log(node.childNodes[i]);
}
```

查找元素：

* document.getElementsByTagName
* document.getElementsByClassNmae
* document.getElementById

注：

* 同上面，因为id是唯一的，所以Element是单数，通过Tag/Class获取的元素一般是多个，所以Elements是复数
* 另外，比如Tag/Class等可以如document.body.getElementsByTagName，但是ById只能在document下 TODO

修改文档：

* removeChild: 从文档中删除指定节点
* appendChild: 添加指定节点到文档末尾
* insertBefore: 将第一个参数的节点插入到第二个参数的节点之前
* replaceChild: 将第一个参数的节点替换为另一个节点

注：将节点插入到某处的副作用是会将其从当前位置移除

创建节点：

* document.createElement
* document.createTextNode

访问属性：

* getAttribute
* setAttribute

HTML允许给节点自定义任何属性，都可以通过上面的方法来访问。

TODO: 「我们可以通过元素的DOM对象的同名属性去访问元素的某些属性，比如链接的href属性。但只有常用的标准属性中很少的一部分是这样的。」是指只有小部分标准属性是可以访问的？

布局：

元素一般分为块(Block)元素和内敛(inline)元素。

JS可以访问元素的尺寸与位置。

* 属性offsetWidth: 元素的起始位置(单位是px)
* 属性offsetHeight: 同上
* 属性clientWidth: 元素内部占据的空间尺寸(不包括padding, border, margin)
* 属性clientHeight: 同上
* 方法getBoundingClientRect(): 返回一个对象，包含top/left/bottom/right和height/width属性，可以精确的顶一个一个元素。注意这些属性的值都是以border外边沿为主。

操作节点的样式：

对于样式直接定义在HTML的节点上，JS可以通过节点的style属性操作元素的样式。如body.style.color, 对于一些样式属性名，如`font-family`，可以写为body.style['font-family']或者body.style.fontFamily(即破折号移除，破折号后第一个字母大写)。

```javascript
<p style="color: purple; font-family: fantasy">
  Pretty Text
</p>

<script>
  "use strict";

  var para = document.body.getElementsByTagName("p")[0];
  console.log(para.style['font-family']);
  //console.log(para.style.fontFamily);
  para.style['font-family'] = "sans-serif";
  //para.style.fontFamily = "sans-serif";
  console.log(para.style.fontFamily);
</script>
```

查询选择器：

* querySelectorAll: document对象和元素节点都定义了此方法，接收一个选择器字符串并返回类数组的对象
* querySelector: 只返回第一个匹配的元素

此方法不随文档变化而动态更新。

浏览器支持我们将函数注册为特定事件(如鼠标、键盘操作等)的处理器。(底层系统给予了在事件发生时响应的机会)

每个DOM元素都有自己的`addEventListener`方法，支持在特定元素上监听事件。

* addEventListener
* removeEventListener

事件触发时会为事件处理函数传递`事件对象`，事件对象有很多属性，比如`type`是表示事件的字符串("click", "mousedown"等)。

```javascript
<button>Click me</button>

<script>
// 按一次后就删除事件
var button = document.querySelector("button");
function once(event) {
  console.log("Button clicked");
  // console.log(event.type);
  // console.log(event);
  button.removeEventListener("click", once);
}
</script>
button.addEventListener("click", once);
```

`传播(propagation)`：若节点含有子节点，则在节点上注册的事件处理器也会接收到在子节点中发生的事件。事件是向外传播的，从触发事件的节点到其父节点，最终直到文档根节点。可以通过调用**事件对象**的`stopPropagation`来阻止事件进一步传播。

```javascript
<p>A paragraph with a <button>button</button>.</p>

<script>
// 按鼠标右键时阻止此事件传播，段落p收不到；其它事件p和button都能收到
var para = document.querySelector("p");
var button = document.querySelector("button");
para.addEventListener("mousedown", function() {
  console.log("Handler for paragraph.");
});
button.addEventListener("mousedown", function(event) {
  console.log("Handler for button.");
  if (event.which == 3)
    event.stopPropagation();
});
</script>
```

事件对象的`target`属性，指向事件的来源节点。

大多数事件都有与其关联的**默认动作**，如点击链接会跳转到相应页面。对于大多数类型的事件，JS事件处理器会在默认处理器执行前被调用，如果事件处理器不想执行默认行为，则可以调用事件对象的`preventDefault`方法。

```javascript
<a href="https://developer.mozilla.org/">MDN</a>

<script>
// 禁止链接的默认事件处理器
var link = document.body.querySelector("a");
link.addEventListener("click", function(event) {
  console.log("Nope.");
  event.preventDefault();
});
</script>
```

一些事件：

* keydown / keyup : keyCode属性是按键值, 通过charCodeAt方法找到按键对应的keyCode值。
* keypress : 在keydown之后触发，只获得按键的输入
* mousedown / mouseup
* click / dbclick : 在mouseup事件之后触发
* mousemove / mouseover / mouseout
* scroll : 滚动事件
* focus / blur : 焦点事件

定时器方法：

* setTimeout: 定时调度, 等待多少毫秒之后执行函数
* clearTimeout: 参数是setTimeout的返回值
* setInterval: 计时器, 每隔一定毫秒数重复执行一次
* clearInterval: 同上，参数是setInterval的返回值

URL编码：使用一个百分号和16进制的数字对字符进行编码：

* encodeURI / decodeURL
* encodeURLComponent / decodeURLComponent

`encodeURI` 假设输入是一个完整的URI，一些特殊字符需要编码；而`encodeURLComponent`则会编码所有的特殊字符。

```javascript
> encodeURIComponent('Hello & World');
'Hello%20%26%20World'

> decodeURIComponent('Hello%20%26%20World');
'Hello & World'

> encodeURI("https://tankywoo.com/Hello & World")
'https://tankywoo.com/Hello%20&%20World'
```

`XMLHttpRequest`: JS发送HTTP请求的接口(注意大小写)

```javascript
var req = new XMLHttpRequest();
req.open("GET", "/test.txt", false);
req.send(null);
console.log('responseText: ', req.responseText);
console.log('status: ', req.status);
console.log('Content-Type: ', req.getResponseHeader('Content-Type'));
```

请求对象的`open`方法配置请求，第三个参数false表示同步请求，true表示异步请求。 对于`GET`请求，`send`方法发送null就可以了。


上面头信息不区分大小写，content-type也可以。另外`setRequestHeader`用于配置请求头。

另外对于xhr, 如果是跨域的请求，需要配置`Access-Control-Allow-Origin`，明确告诉浏览器网站向其它域发送请求没问题，否则浏览器console会报错。

对于异步请求：

下面给请求对象加上事件处理器，表示数据ok后提醒前台代码：

```javascript
var req = new XMLHttpRequest();
req.open("GET", "/test.txt", true);
req.addEventListener("load", function() {
  console.log("Done: ", req.status);
});
req.send(null);
```

## TODO

* 未定义值null和undefined不等价的情况?
* 函数 - 闭包
* 创建对象的另外一种方式?
* JS 正则
* 第十章 模块
