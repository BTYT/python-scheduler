# python-scheduler
demo to show how to work with apscheduler.

另外一个使用此脚本的场景：
从数据库中删除数据。 
为了避免sql长时间执行一直占用cpu， 需要先select一部分id，然后再delete WHERE id IN ()，然后再select，再delete，循环下去

话说做为RD，权限非常小， 否则就可以安装一些tools到db里面， 也就不用这么费劲了。
比如以前作DBA的时候最常使用的：http://code.openark.org/blog/tag/common_schema

