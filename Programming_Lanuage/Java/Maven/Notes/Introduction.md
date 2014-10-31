# Apache Maven学习总结

## 前言

Maven，发音是[`meivin]，"专家"的意思。它由Apache软件基金会所提供，曾是Jakarta项目的子项目。是一个软件（特别是Java软件）项目管理及自动构建工具。Maven 基于项目对象模型（缩写：POM）概念，Maven利用一个中央信息片断能管理一个项目的构建、报告和文档等步骤:

- 版本（version）
    - Maven有自己的版本定义和规则
- 构建（build）
    - Maven支持许多中的应用程序类型，对于每一种支持的应用程序类型都定义好了一组构建规则和工具集。
- 文档和构建结果
    - maven的site命令支持各种文档信息的发布，包括构建过程的各种输出，javadoc，产品文档等。
- 测试
- 打包
- 集成测试
- 验证
- 项目关系
    - 一个大型的项目通常有几个小项目或者模块组成，用maven可以很方便地管理 
- 移植性管理
    - maven可以针对不同的开发场景，输出不同种类的输出结果。
- 部署

## 常用命令

命令|说明|更多
----|----|---
mvn -version/-v|版本信息|-
mvn archetype|mvn archetype:generate/create -DarchetypeGroupId=org.apache.maven.archetypes -DgroupId=com.mycompany.app -DartifactId=my-app|[archetype官方介绍](http://maven.apache.org/guides/introduction/introduction-to-archetypes.html)
mvn package|生成target目录，编译、测试代码，生成测试报告，生成jar/war文件|-
mvn jetty:run|运行项目于jetty上|-
mvn compile|编译|-
mvn test|编译并测试|-
mvn clean|清空生成的文件|-
mvn site|生成项目相关信息的网站|-
mvn eclipse:eclipse|将项目转化为Eclipse项目|-
mvn -Dwtpversion=1.0 eclipse:eclipse|生成Wtp插件的Web项目|-
mvn -Dwtpversion=1.0 eclipse:clean|清除Eclipse项目的配置信息（Web项目）|-

## Maven的版本规范

maven使用如下几个要素来唯一定位某一个输出物： groupId:artifactId:packaging:version 。比如org.springframework:spring:2.5 。每个部分的解释如下：

- groupId：
    - 团体，公司，小组，组织，项目，或者其它团体。团体标识的约定是，它以创建这个项目的组织名称的逆向域名(reverse domain name)开头。来自Sonatype的项目有一个以com.sonatype开头的groupId，而Apache Software的项目有以org.apache开头的groupId。
- artifactId：
    - 在groupId下的表示一个单独项目的唯一标识符。比如我们的tomcat, commons等。不要在artifactId中包含点号(.)。
- packaging
    - 项目的类型，默认是jar，描述了项目打包后的输出。类型为jar的项目产生一个JAR文件，类型为war的项目产生一个web应用。
- version
    - 一个项目的特定版本。发布的项目有一个固定的版本标识来指向该项目的某一个特定的版本。而正在开发中的项目可以用一个特殊的标识，这种标识给版本加上一个"SNAPSHOT"的标记。 
- classifier
    - 很少使用的坐标，一般都可以忽略classifiers。如果你要发布同样的代码，但是由于技术原因需要生成两个单独的构件，你就要使用一个分类器（classifier）。例如，如果你想要构建两个单独的构件成JAR，一个使用Java 1.4编译器，另一个使用Java 6编译器，你就可以使用分类器来生成两个单独的JAR构件，它们有同样的groupId:artifactId:version组合。如果你的项目使用本地扩展类库，你可以使用分类器为每一个目标平台生成一个构件。分类器常用于打包构件的源码，JavaDoc或者二进制集合。

**Maven有自己的版本规范**，一般是如下定义 <major version\>.<minor version\>.<incremental version\>-<qualifier\> ，比如1.2.3-beta-01。要说明的是，maven自己判断版本的算法是major,minor,incremental部分用数字比较，qualifier部分用字符串比较，所以要小心 alpha-2和alpha-15的比较关系，最好用 alpha-02的格式。 

Maven在版本管理时候可以使用几个特殊的字符串 SNAPSHOT ,LATEST ,RELEASE 。比如"1.0-SNAPSHOT"。各个部分的含义和处理逻辑如下说明： 

- SNAPSHOT 
    - 如果一个版本包含字符串"SNAPSHOT"，Maven就会在安装或发布这个组件的时候将该符号展开为一个日期和时间值，转换为UTC时间。例如，"1.0-SNAPSHOT"会在2010年5月5日下午2点10分发布时候变成1.0-20100505-141000-1。 
    - 这个词只能用于开发过程中，因为一般来说，项目组都会频繁发布一些版本，最后实际发布的时候，会在这些snapshot版本中寻找一个稳定的，用于正式发布，比如1.4版本发布之前，就会有一系列的1.4-SNAPSHOT，而实际发布的1.4，也是从中拿出来的一个稳定版。 
- LATEST 
    - 指某个特定构件的最新发布，这个发布可能是一个发布版，也可能是一个snapshot版，具体看哪个时间最后。 
- RELEASE 
    - 指最后一个发布版。 

## Maven的依赖管理（dependencies）

依赖管理一般是最吸引人使用maven的功能特性了，这个特性让开发者只需要关注代码的直接依赖，比如我们用了spring，就加入spring依赖说明就可以了，至于spring自己还依赖哪些外部的东西，maven帮我们搞定。

任意一个外部依赖说明包含如下几个要素：**groupId**, **artifactId**, **version**, **scope**, **type**, **optional**。其中前3个是必须的，各自含义如下：

- groupId: 必须 
- artifactId: 必须 
- version: 必须。 
    - 这里的version可以用区间表达式来表示，比如(2.0,)表示>2.0，[2.0,3.0)表示2.0<=ver<3.0；多个条件之间用逗号分隔，比如[1,3),[5,7]。 
- scope 作用域限制 
- type 一般在pom引用依赖时候出现，其他时候不用 
- optional 是否可选依赖 

Maven认为，程序对外部的依赖会随着程序的所处阶段和应用场景而变化，所以maven中的依赖关系有作用域(scope)的限制。在maven中，scope包含如下的取值：

- compile（编译范围） 
    - compile是默认的范围；如果没有提供一个范围，那该依赖的范围就是编译范围。编译范围依赖在所有的classpath中可用，同时它们也会被打包。 
- provided（已提供范围） 
    - provided依赖只有在当JDK或者一个容器已提供该依赖之后才使用。例如，如果你开发了一个web应用，你可能在编译classpath中需要可用的Servlet API来编译一个servlet，但是你不会想要在打包好的WAR中包含这个Servlet API；这个Servlet API JAR由你的应用服务器或者servlet容器提供。已提供范围的依赖在编译classpath（不是运行时）可用。它们不是传递性的，也不会被打包。 
- runtime（运行时范围） 
    - runtime依赖在运行和测试系统的时候需要，但在编译的时候不需要。比如，你可能在编译的时候只需要JDBC API JAR，而只有在运行的时候才需要JDBC驱动实现。 
- test（测试范围） 
    - test范围依赖 在一般的 编译和运行时都不需要，它们只有在测试编译和测试运行阶段可用。 
- system（系统范围） 
    - system范围依赖与provided类似，但是你必须显式的提供一个对于本地系统中JAR文件的路径。这么做是为了允许基于本地对象编译，而这些对象是系统类库的一部分。这样的构件应该是一直可用的，Maven也不会在仓库中去寻找它。 如果你将一个依赖范围设置成系统范围，你必须同时提供一个**systemPath**元素 。注意该范围是不推荐使用的（你应该一直尽量去从公共或定制的Maven仓库中引用依赖）。

## 多项目管理

maven的多项目管理也是非常强大的。一般来说，maven要求同一个工程的所有子项目都放置到同一个目录下，每一个子目录代表一个项目，比如

    总项目/ 
        pom.xml 总项目的pom配置文件 
        子项目1/ 
            pom.xml 子项目1的pom文件 
        子项目2/ 
            pom.xml 子项目2的pom文件

按照这种格式存放，就是继承方式，所有具体子项目的pom.xml都会继承总项目pom的内容，取值为子项目pom内容优先。

要设置继承方式，首先要在总项目的pom中加入如下配置:

```xml
<modules> 
    <module>simple-weather</module> 
    <module>simple-webapp</module> 
</modules>
```

其次在每个子项目中加入如下配置即可 :

```xml
<parent> 
    <groupId>org.sonatype.mavenbook.ch06</groupId> 
    <artifactId>simple-parent</artifactId> 
    <version>1.0</version> 
</parent>
```

当然，继承不是唯一的配置文件共用方式，maven还支持引用方式。引用pom的方式更简单，在依赖中加入一个type为pom的依赖即可，如下：

```xml
<project> 
    <description>This is a project requiring JDBC</description> 
    ... 
    <dependencies> 
        ... 
        <dependency> 
            <groupId>org.sonatype.mavenbook</groupId> 
            <artifactId>persistence-deps</artifactId> 
            <version>1.0</version> 
            <type>pom</type> 
        </dependency> 
    </dependencies> 
</project> 
```

## Maven 属性定义

用户可以在maven中定义一些属性，然后在其他地方用${xxx}进行引用。比如：

```xml
<project> 
    <modelVersion>4.0.0</modelVersion> 
    ... 
    <properties> 
        <var1>value1</var1> 
    </properties> 
</project>
```

maven提供了三个隐式的变量，用来访问系统环境变量、POM信息和maven的settings：

- env
    - 暴露操作系统的环境变量，比如env.PATH 
- project 
    - 暴露POM中的内容，用点号(.)的路径来引用POM元素的值，比如${project.artifactId}。另外，java的系统属性比如user.dir等，也暴露在这里。 
- settings 
    - 暴露maven的settings的信息，也可以用点号(.)来引用。maven把系统配置文件存放在maven的安装目录中，把用户相关的配置文件存放在~/.m2/settings.xml(unix)或者%USERPROFILE%/.m2/settings.xml(windows)中。

## Maven的profile

profile是maven的一个重要特性，它可以让maven能够自动适应外部的环境变化，比如同一个项目，在linux下编译linux的版本，在win下编译win的版本等。一个项目可以设置多个profile，也可以在同一时间设置多个profile被激活（active）的。自动激活的 profile的条件可以是各种各样的设定条件，组合放置在activation节点中，也可以通过命令行直接指定。profile包含的其他配置内容可以覆盖掉pom定义的相应值。如果认为profile设置比较复杂，可以将所有的profiles内容移动到专门的 profiles.xml 文件中，不过记得和pom.xml放在一起。

activation节点中的激活条件中常见的有如下几个：

- **os**：判断操作系统相关的参数，它包含如下可以自由组合的子节点元素 
    - message - 规则失败之后显示的消息 
    - arch - 匹配cpu结构，常见为x86 
    - family - 匹配操作系统家族，常见的取值为：dos，mac，netware，os/2，unix，windows，win9x，os/400等
    - name - 匹配操作系统的名字 
    - version - 匹配的操作系统版本号 
    - display - 检测到操作系统之后显示的信息
- **jdk**
    - 检查jdk版本，可以用区间表示。
- **property**
    - 检查属性值，本节点可以包含name和value两个子节点。
- **file**
    - 检查文件相关内容，包含两个子节点：exists和missing，用于分别检查文件存在和不存在两种情况。

更多参见[Maven profile setting](http://maven.apache.org/guides/introduction/introduction-to-profiles.html)
