## Maven 简要介绍
---
### 下载和安装
* http://maven.apache.org/download.cgi 进行下载 ，maven是java语言编写的
* 解压后看到如下结构：
  * bin：可执行命令；
  * boot：plexus-classworlds-xxx.jar 是一个自定义的类加载器框架。
  * conf：mavaen的配置文件（settings.xml），建议放到**～/.m2/**目录下
  * lib：maven运行时的类库
  
### 概念
* maven核心是一个空的“容器”，正是因为空才是他的强大，可以安装各种各样的插件。
  * 比如：第一次使用mvn install，会自动从远程资源库下载大部分核心的maven插件
* POM文件是Project Object Model项目对象模型描述文件，用于描述：
  * 该项目是什么类型？ 
  * 该项目的名称？
  * 该项目的构建功能？
 * maven的坐标（唯一标识）由下面组成：
  * <groupId/>：开发者公司的域名
  * <artifactId/>：项目名称
  * <packaging/>：打包类型
  * <version/>：版本号
  * groupId:artifactId:packaging:version -> junit:junit:jar:3.8.1
 * Maven的原则：**约定优于配置（Convention over Configuation）**，约定内容如下：
  * 源代码位于：{basedir}/src/main/java/
  * 测试代码位于：{basedir}/src/test
  * 资源文件位于：{basedir}/src/main/resouerces
  * 编译生成的文件：：{basedir}/target/classes
  * 生成的jar包：{basedir}/target
  * 当然如果要修改，也可以修改
* maven的资源库repository：搜索顺序 本地 -> 远程 -> 中央 ，一旦找到就下载到本地资源库；
  * 本地资源库：本机维护
  * 远程资源库：公司内部维护
  * 中央资源库：maven官方维护


### 生命周期
* Maven的三个基本生命周期：**clean、default 和 site**
* clean生命周期用于在构建项目之前进行一些清理工作，包含三个核心阶段：
  * pre-clean：构建之前的预清理；
  * clean：执行清理；
  * post-clean：最后清理；
  * 上述命令执行后会清理项目编译过程生成的文件，只剩src目录和pom文件；
* default生命周期包含项目构建的核心部分：
  * compile：编译项目
  * test：单元测试
  * packaging：打包项目
  * install：安装到本地仓库
  * deploy：部署到远程仓库
  * 实际上除了上述核心阶段还有很多阶段
* site生命周期：
  * pre-site：生成站点
  * site：做验证
  * site-deploy：发布站点到远程服务器
* 软件构建的生命周期：compile -> test -> packaging -> install -> deploy
* 不管运行哪一个阶段的命令（如mvn install），自动执行**从生命周期的第一个阶段开始，直至mvn命令指定的阶段**
* 可以使用<phase>指定某个阶段使用哪个插件
  
### 依赖管理
* Maven
