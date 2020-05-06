Redis 基础入门教学实践
--------------
### 1、 简介
* Redis: 全称为 REmote DIctionary Server(远程字典服务)
* 是完全开源免费的，用C语言编写的，遵守BSD协议，高性能的(key/value)分布式内存数据库，基于**内存运行**并支持持久化的NoSQL数据库.

### 2、下载和安装
* 下载：官网直接下载[https://redis.io](https://redis.io)
* 安装：
  * 官网下载tar包安装：安装GCC；上传redisxx-xx.tar.gz包;解压tar.gz包；make PREFIX=/usr/local/redis install 编译；
  * yum安装： yum install redis；

切换到 /usr/local/redis/bin目录下，可以看到如下5个工具
``` Java
    ①、redis-server：Redis服务器

　　②、redis-cli：Redis命令行客户端

　　③、redis-benchmark：Redis性能测试工具

　　④、redis-check-aof：AOF文件修复工具

　　⑤、redis-check-rdb：RDB文件检查工具
```

### 3、配置
* 配置文件管理： 为了方便管理，把redis.conf复制到 /etc/redis/redis.conf
* 


### 4、启动
* 前台窗口方式启动：
```
/redis-server /etc/redis/redis.conf
```
* 后台自动运行：
```
redis.conf 文件中，设置  daemonize yes
```
* 查询是否运行（进程）：
```
ps -ef | grep redis
```
* 运行成功后启动客户端，可以进行一些交互式操作了
```
redis-cli
```

### 5、
