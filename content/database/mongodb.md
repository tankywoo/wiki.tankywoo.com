---
title: "MongoDB"
date: 2016-09-16 14:00
updated: 2017-08-08 17:55
logs: "补充认证相关"
---

[TOC]

[MongoDB官方文档](https://docs.mongodb.com/manual/)

## 常用命令

### 插入数据

```text
db.users.insert({'username': 'tankywoo', 'email': 'me@tankywoo.com', 'name': 'TankyWoo', 'password_hash': 'pbkdf2:sha1:1000$pPfqG458$6f79c72df67897b1234abcdcc4helloworldhehe'})
```

### 用户认证

目前最新的稳定版是 3.X 版本，认证这块改动还是非常大：

首先，认证机制由 `MONGODB-CR` 改为 `SCRAM-SHA-1`，[参考](https://docs.mongodb.com/manual/release-notes/3.0-scram/#upgrade-2-6-mongodb-cr-users-to-scram-sha-1)，具体看[这里](https://docs.mongodb.com/manual/core/authentication-mechanisms/)

创建用户的命令也变了，改用 `db.createUser()`

最后，用户的角色也变得非常复杂，比如针对数据库用户、数据库管理员、超级管理员等等，具体看 [Built-In Roles](https://docs.mongodb.com/manual/reference/built-in-roles/#all-database-roles)

大致的步骤就是：

- 先关闭认证，切换到 admin 数据库
- 创建管理员用户，用于后续针对数据库创建的读写用户
- 开启认证，使用管理员登录
- 切换到欲创建的数据库，创建用户，授予如 `readWrite` 角色使其可以读写

注：一个用户可以配置多个角色，比如我使用 [mongo-hacker](https://github.com/TylerBrock/mongo-hacker) 会在 `find` 后读取 profile 信息，而这个信息需要 `dbAdmin` 角色读，所以我最后给用户 `readWrite` 和 `dbAdmin` 两个角色：

```text
> show users
{
  "_id": "mydb.myuser",
  "user": "myuser",
  "db": "mydb",
  "roles": [
    {
      "role": "dbAdmin",
      "db": "mydb"
    },
    {
      "role": "readWrite",
      "db": "mydb"
    }
  ]
}

```

还可以参考这篇 [博文](http://tgrall.github.io/blog/2015/02/04/introduction-to-mongodb-security/)，更详细可以看官方文档 [Enable Auth](https://docs.mongodb.com/manual/tutorial/enable-authentication/)


以下是 MongoDB 2.x 的用户认证相关：

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
