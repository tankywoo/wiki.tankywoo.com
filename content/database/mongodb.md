---
title: "MongoDB"
date: 2016-09-16 14:00
updated: 2016-09-24 23:00
logs: "更新多级字典修改某列操作"
---

[TOC]

[MongoDB官方文档](https://docs.mongodb.com/manual/)

## 常用命令

### 插入数据

```text
db.users.insert({'username': 'tankywoo', 'email': 'me@tankywoo.com', 'name': 'TankyWoo', 'password_hash': 'pbkdf2:sha1:1000$pPfqG458$6f79c72df67897b1234abcdcc4helloworldhehe'})
```

### 用户认证

首先先添加一个管理员帐号

```text
> use admin
switched to db admin

> db.addUser("root", "123456");
WARNING: The 'addUser' shell helper is DEPRECATED. Please use 'createUser' instead
Successfully added user: { "user" : "tankywoo", "roles" : [ "root" ] }
```

给普通数据库添加帐号：

```text
> use mytest
switched to db mytest

> db.addUser("tankywoo", "123456");
WARNING: The 'addUser' shell helper is DEPRECATED. Please use 'createUser' instead
Successfully added user: { "user" : "tankywoo", "roles" : [ "dbOwner" ] }
```

然后修改`mongodb.conf`，添加配置：

```text
security:
  authorization: enabled
```

重启MongoDB

认证：

```text
> db.auth('username', 'password');
```

**注** : 普通用户权限(绑定到数据库)，需要先`use dbname`切换到指定数据库，再认证。

### 更新整个文档

```text
mycollection.update({'_id':mongo_id}, {"$set": post}, upsert=False)
```

参考:

* [How do I update a Mongo document after inserting it?](http://stackoverflow.com/questions/4372797/how-do-i-update-a-mongo-document-after-inserting-it)
* [How do I partially update an object in MongoDB so the new object will overlay / merge with the existing one](http://stackoverflow.com/questions/10290621/how-do-i-partially-update-an-object-in-mongodb-so-the-new-object-will-overlay)


### collection增加一列

```text
> db.coll.update({}, {$set: {'data': {}}}, false, true)
Updated 2 existing record(s) in 2ms
WriteResult({
  "nMatched": 2,
  "nUpserted": 0,
  "nModified": 2
})
```

参考：[Add new field to a collection in MongoDB](http://stackoverflow.com/questions/7714216/add-new-field-to-a-collection-in-mongodb)


### 修改某一个文档的某一列值

比如多级字典：

```text
> db.coll.update({'_id': ObjectId('123405ff3b909e19269a381a')}, {$set: {'data': {'2016-09-24': true}}})
```

或者（这种比较方便）：

```text
> db.coll.update({'_id': ObjectId('123405ff3b909e19269a381a')}, {$set: {'data.2016-09-24': true}} )
```

参考：[MongoDB: update dictionary in document](http://stackoverflow.com/questions/29267519/mongodb-update-dictionary-in-document)


## Cheat Sheet

* [MongoDB-CheatSheet-v1_0.pdf](chrome-extension://ikhdkkncnoglghljlkmcimlnlhkeamad/pdf-viewer/web/viewer.html?file=https%3A%2F%2Fblog.codecentric.de%2Ffiles%2F2012%2F12%2FMongoDB-CheatSheet-v1_0.pdf)
* [MongoDB Cheat Sheet by ovi_mihai](https://www.cheatography.com/ovi-mihai/cheat-sheets/mongodb/)
* [MongoDB Cheat Sheet – Quick Reference](http://www.mongodbspain.com/en/2014/03/23/mongodb-cheat-sheet-quick-reference/)
