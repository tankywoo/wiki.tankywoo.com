---
title: "Python 进程/线程"
date: 2013-08-22 23:48
---



## Python的伪多线程 ##

TODO

相关讨论:

* [py的多线程是伪线程吗?](http://bbs.chinaunix.net/thread-1264893-1-1.html)
* [[Python-3000] the future of the GIL](http://mail.python.org/pipermail/python-3000/2007-May/007414.html)
* [Python多线程的问题](http://bbs.csdn.net/topics/390226723)

## 相关的模块 ##

* thread
* threading
* Queue
* multiprocessing


### Queue ###

Queue模块主要有三种队列实现

* Queue(FIFO)
* LifoQueue
* PriorityQueue

Queue是线程同步的


### threading ###

PyMOTW [Manege concurrent threads](http://www.doughellmann.com/PyMOTW/threading/index.html)

在看上面链接的第一个代码时，遇到了一个`print`和`sys.stdout.write`的问题<br />
具体见 TODO

最简单的threading配合Queue的Example

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    # wutq@2013-02-18
    # Python参考手册 P363

    import threading
    from Queue import Queue

    class WorkThread(threading.Thread):
    	def __init__(self, *args, **kwargs):
    		threading.Thread.__init__(self, *args, **kwargs)
    		self.input_queue = Queue()

    	def send(self, item):
    		self.input_queue.put(item)

    	def close(self):
    		#在队列上设置一个标志，使线程在处理完毕后关闭
    		self.input_queue.put(None)
    		self.input_queue.join()

    	def run(self):
    		while True:
    			item = self.input_queue.get()
    			if item is None:
    				break
    			print item
    			self.input_queue.task_done()
    		self.input_queue.task_done()
    		return

    w = WorkThread()
    w.start()
    w.send("hello")
    w.send("world")
    w.close()


在StackOverflow上也找到一篇帖子: [python multithreading for dummies](http://stackoverflow.com/questions/2846653/python-multithreading-for-dummies)
里面也提到了

    CPython can use threads only for *I\O waits* due to *GIL*. 
    If you want to benefit from multiple cores for CPU-bound tasks, use *mutliprocessing*


## 线程池 ##
线程池概念

    所谓的线程池就是完成一种任务的一组线程
    一般情况下是首先初始化一定数量的工作线程，并把任务提交给空闲的线程
    当线程都处于忙的状态的时候，则重新生成新的工作线程
    当空闲线程较多的时候则停止一部分线程
    这些要看具体的调度算法。
    但是线程不能滥用，因为并不是线程越多就会带来更好的性能

参考:

* [线程池概念讨论](http://bbs.csdn.net/topics/50024963)
* [线程池的概念及Linux 怎么设计一个简单的线程池](http://blog.chinaunix.net/uid-26983585-id-3336491.html)

一个不错的Example

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    import Queue
    import threading
    import time

    class WorkManager(object):
        def __init__(self, work_num=1000,thread_num=2):
            self.work_queue = Queue.Queue()
            self.threads = []
            self.__init_work_queue(work_num)
            self.__init_thread_pool(thread_num)

        def __init_work_queue(self, jobs_num):
            """初始化工作队列"""
            for i in range(jobs_num):
                self.add_job(do_job, i)

        def __init_thread_pool(self,thread_num):
            """初始化线程"""
            for i in range(thread_num):
                self.threads.append(Work(self.work_queue))

        def add_job(self, func, *args):
            """添加一项工作入队"""
            #任务入队，Queue内部实现了同步机制
            self.work_queue.put((func, list(args)))

        def check_queue(self):
            """检查剩余队列任务"""
            return self.work_queue.qsize()

        def wait_allcomplete(self):
            """等待所有线程运行完毕"""
            for item in self.threads:
                if item.isAlive():item.join()

    class Work(threading.Thread):
        def __init__(self, work_queue):
            threading.Thread.__init__(self)
            self.work_queue = work_queue
            self.start()

        def run(self):
            while True:
                try:
                    #任务异步出队，Queue内部实现了同步机制
                    do, args = self.work_queue.get(block=False)
                    do(args)
                    self.work_queue.task_done()#通知系统任务完成
                except Exception,e:
                    print str(e)
                    break

    #具体要做的任务
    def do_job(args):
        #print args
        time.sleep(0.1)#模拟处理时间
        #print threading.current_thread(), list(args)

    if __name__ == '__main__':
        for thread_num in (10, 20):
            print "Thread Num: %d" % thread_num
            start = time.time()
            work_manager =  WorkManager(500, thread_num)
            work_manager.wait_allcomplete()
            end = time.time()
            print "cost all time: %s" % (end-start)

来源: http://www.open-open.com/home/space-5679-do-blog-id-3247.html

略做了一点修改

网上关于线程池不错的文章:
* [python线程池](http://www.the5fire.net/python-thread-pool.html)
* [python线程池的实现](http://www.handaoliang.com/a/20071102/184706.html)
* [python threadpool第三方模块](http://www.chrisarndt.de/projects/threadpool/)

