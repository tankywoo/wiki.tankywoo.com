---
title: "JavaScript"
date: 2016-08-21 22:29
updated: 2016-08-21 22:29
tag: javascript
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
