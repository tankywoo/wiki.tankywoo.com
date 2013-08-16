<!-- title : Python Performance Analysis Tool -->

# Python 性能分析工具 #

# timeit #

timeit 模块提供了简单的接口来测量小段代码的执行时间.

	import timeit

	t = timeit.Timer("print 'main statement'", "print 'setup'")

	print 'TIMEIT:'
	print t.timeit(2)

	print 'REPEAT:'
	print t.repeat(3, 2)

timeit的Timer类接口分别是一个要执行的语句和初始化语句, timeit成员函数提供一个反复执行语句的次数(默认1000000次)和重复执行timeit的次数.

# profile #

# pstats #

# 修改历史 #

* 2013-07-05 : 增加timeit
