---
title: "JavaScript"
date: 2016-08-21 22:29
updated: 2016-09-24 23:30
tag: javascript
log: "增加click实践在ajax下失效问题"
---

[TOC]


## Tips

### 如何复制一个对象

涉及到深复制和浅复制的问题

参考SO上回答：[What is the most efficient way to clone an object in JavaScript?](http://stackoverflow.com/questions/122102/what-is-the-most-efficient-way-to-clone-an-object-in-javascript)

最简单的答案，通过jQuery来处理。注意我之前在搜相关API时，也看到下面提到的clone这个方法，不过看文档说是针对DOM的。

I want to note that the [`.clone()`](http://api.jquery.com/clone/) method in jQuery only clones DOM elements. In order to clone JavaScript objects, you would do:

```javascript
// Shallow copy
var newObject = jQuery.extend({}, oldObject);

// Deep copy
var newObject = jQuery.extend(true, {}, oldObject);
```

More information can be found in the [jQuery documentation](http://api.jquery.com/jQuery.extend/).

I also want to note that the deep copy is actually much smarter than what is shown above – it's able to avoid many traps (trying to deep extend a DOM element, for example). It's used frequently in jQuery core and in plugins to great effect.

其它参考：

* [javascript中的深拷贝和浅拷贝？](https://www.zhihu.com/question/23031215)
* [在javascript里怎样方便的克隆一个object](https://segmentfault.com/q/1010000000148290)


### click事件在Ajax下失效问题

最开始给一个click事件写一个Ajax，更新#board的html内容：

```javascript
$('#board').click(function(){
	$.ajax() {
		...
	}
})
```

但是在点击一次后，后续点击就不再触发click事件了。

搜了下，针对`.click()`，因为ajax中有replace替换了原来绑定了这个事件的元素(element)，所以导致失效。

`.on()`方法使用`事件代理(event delegation)`，可以保证在动态元素上：

```javascript
$('document').on("click", "#board", function(){
	$.ajax() {
		...
	}
})
```

参考：

* [Jquery Event wont fire after ajax call](http://stackoverflow.com/questions/13767919/jquery-event-wont-fire-after-ajax-call)
* [jQuery click() event not firing on AJAX loaded HTML elements](http://stackoverflow.com/questions/9272438/jquery-click-event-not-firing-on-ajax-loaded-html-elements)
