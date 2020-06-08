# Kafka总结
----
### kafka总体架构
* 画一下总体架构？
* 解释名词Producer、Broker、push 、Partition、Consumer、Consumer group、replica、leader、follower、controller、ZooKeeper
* Topic & Partition关系？存储层面？关系图？为什么要这样划分？怎么配置?生成的文件什么样的？
* Partition能不能再划分？为什么要这样?更小部分的工作原理是什么？画一下工作原理图？
* 如何从 partition 中通过 offset 查找 message 呢？
* 复制原理和同步方式？如何确保新选举出的 leader 是优选呢？？HW、LEO、ISR、OSR？画一下流转图？
* 数据可靠性和持久性保证？如何在保证可靠性的前提下避免吞吐量下降？选举策略?
*  Kafka 架构中 ZooKeeper 以怎样的形式存在？broker\topic\consumer\producer怎么注册的？producer/consumer怎么负载均衡?
*  how记录消费进度?why记录 Partition 与 Consumer 的关系?
* 全程解析（Producer-kafka-consumer）??



具体到Kafka而言，它使用了基于日志结构(log-structured)的数据格式，即每个分区日志只能在尾部追加写入(append)，而不允许随机“跳到”某个位置开始写入，故此实现了顺序写入。

https://blog.csdn.net/qq_37142346/article/details/91349100