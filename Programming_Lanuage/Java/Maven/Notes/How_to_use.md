# Maven的操作和使用

maven的操作有两种方式，一种是通过mvn命令行命令，一种是使用maven的eclipse插件。这里只讲命令行模式

------------

## Maven的配置文件

maven的主执行程序为mvn.bat，linux下为mvn.sh，这两个程序都很简单，它们的共同用途就是收集一些参数，然后用 java.exe来运行maven的Main函数。maven同样需要有配置文件，名字叫做settings.xml，它放在两个地方，一个是maven 安装目录的conf目录下，对所有使用该maven的用户都起作用，我们称为主配置文件，另外一个放在 %USERPROFILE%/.m2/settings.xml下，我们成为用户配置文件，只对当前用户有效，且可以覆盖主配置文件的参数内容。还有就是项目级别的配置信息了，它存放在每一个maven管理的项目目录下，叫pom.xml，主要用于配置项目相关的一些内容，当然，如果有必要，用户也可以在 pom中写一些配置，覆盖住配置文件和用户配置文件的设置参数内容。 

一般来说，settings文件配置的是比如repository库路径之类的全局信息，具体可以参考[官方文章](http://maven.apache.org/ref/2.2.1/maven-settings/settings.html) 。

### Maven有哪些配置文件？都在哪儿定义？

- 每个Maven工程
    - pom.xml
- 每个用户
    - (%USER_HOME%)/.m2/settings.xml
- 全局
    - (%M2_HOME%)/conf/settings.xml
- profile描述
    - 工程根目录下的profiles.xml（Maven3.0不再支持）

-----------

## 创建新工程

要创建一个新的maven工程，我们需要给我们的工程指定几个必要的要素，就是maven产品坐标的几个要素：groupId, artifactId，如果愿意，你也可以指定version和package名称。我们先看一个简单的创建命令：

```sh
mvn archetype:create -DgroupId=org.hello -DartifactId=helloworld -DarchetypeArtifactId=maven-archetype-simple
```

首先看这里的命令行参数的传递结构，怪异的 -D参数=值 的方式是 java.exe 要求的方式。这个命令创建一个简单工程，目录结构是一个标准的maven结构，如下

```tree
├── pom.xml
└── src
    ├── main
    │   └── java
    │       └── org
    │           └── hello
    │               └── App.java
    └── test
        └── java
            └── org
                └── hello
                    └── AppTest.java
```

大家要注意，这里目录结构的布局实际上是由参数 archetypeArtifactId 来决定的，因为这里传入的是 maven-archetype-webapp 如果我们传入其他的就会创建不同的结构，默认值为 maven-archetype-quickstart。选用其他类型可能需要安装相应plug-in。[更多archetype的信息](http://maven.apache.org/guides/introduction/introduction-to-archetypes.html)

----------

## 安装库文件到Maven库中

在maven中一般都会用到安装库文件的功能，一则是我们常用的hibernate要使用jmx库，但是因为sun的license限制，所以无法将其直接包含在repository中。所以我们使用mvn命令把jar安装到我们本地的repository中 

```sh
mvn install:install-file -DgroupId=com.sun.jdmk -DartifactId=jmxtools -Dversion=1.2.1 -Dpackaging=jar -Dfile=/path/to/file 
```

如果我们想把它安装到公司的repository中，需要使用命令：

```sh
mvn deploy:deploy-file -DgroupId=com.sun.jdmk -DartifactId=jmxtools -Dversion=1.2.1 -Dpackaging=jar -Dfile=/path/to/file -Durl=http://xxx.ss.com/sss.xxx -DrepositoryId=release-repo 
```

对于我们的工程输出，如果需要放置到公司的repository中的话，可以通过配置pom来实现：

```xml
<distributionManagement> 
    <repository> 
        <id>mycompany-repository</id> 
        <name>MyCompany Repository</name> 
        <url>scp://repository.mycompany.com/repository/maven2</url> 
    </repository> 
</distributionManagement>
```

这里使用的scp方式提交库文件，还有其他方式可以使用，请参考faq部分。然后记得在你的settings.xml中加入这一内容：

```xml
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0" 
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 
          http://maven.apache.org/xsd/settings-1.0.0.xsd"> 
    ... 
    <servers> 
        <server> 
            <id>mycompany-repository</id> 
            <username>jvanzyl</username> 
            <!-- Default value is ~/.ssh/id_dsa --> 
            <privateKey>/path/to/identity</privateKey> 
            <passphrase>my_key_passphrase</passphrase> 
        </server> 
    </servers> 
    ... 
</settings> 
```

-----------

## Maven的变量

Maven定义了很多变量属性,参考[这里](http://docs.codehaus.org/display/MAVENUSER/MavenPropertiesGuide)

**内置属性**: 

- ${basedir } represents the directory containing pom.xml 
- ${version } equivalent to ${project.version } or ${pom.version }

Pom/Project properties

所有pom中的元素都可以用 project. 前缀进行引用,以下是部分常用的:

- ${project.build.directory } results in the path to your "target" dir, this is the same as ${pom.project.build.directory } 
- ${project.build. outputD irectory } results in the path to your "target/classes" dir 
- ${project.name } refers to the name of the project. 
- ${project.version } refers to the version of the project. 
- ${project.build.finalName } refers to the final name of the file created when the built project is packaged 

本地用户设定

所有用的的 settings.xml 中的设定都可以通过 settings. 前缀进行引用：
- ${settings.localRepository } refers to the path of the user's local repository. 
- ${maven.repo.local } also works for backward compatibility with maven1

**环境变量**

系统的环境变量通过 env. 前缀引用：

- {env.M2_HOME } returns the Maven2 installation path. 
- ${java.home } specifies the path to the current JRE_HOME environment use with relative paths to get for example: 
    - <jvm>${java.home}../bin/java.exe</jvm> 

**java系统属性**

所有JVM中定义的java系统属性. 用户在pom中定义的自定义属性：

```xml
<project> 
    ... 
    <properties> 
        <my.filter.value>hello</my.filter.value> 
    </properties> 
    ... 
</project>
```

则引用 ${my.filter.value } 就会得到值 hello 

**上级工程的变量**

上级工程的pom中的变量用前缀 ${project.parent } 引用. 上级工程的版本也可以这样引用:${parent.version }. 

------------

## Maven的使用 

我们已经知道maven预定义了许多的阶段（phase），每个插件都依附于这些阶段，并且在进入某个阶段的时候，调用运行这些相关插件的功能。我们先来看完整的maven生命周期：


生命周期|阶段描述
-------|---------
validate|验证项目是否正确，以及所有为了完整构建必要的信息是否可用
generate-sources|生成所有需要包含在编译过程中的源代码
process-sources|处理源代码，比如过滤一些值
generate-resources|生成所有需要包含在打包过程中的资源文件
process-resources|复制并处理资源文件至目标目录，准备打包
compile|编译项目的源代码
process-classes|后处理编译生成的文件，例如对Java类进行字节码增强（bytecode enhancement）
generate-test-sources|生成所有包含在测试编译过程中的测试源码
process-test-sources|处理测试源码，比如过滤一些值
generate-test-resources|生成测试需要的资源文件
process-test-resources|复制并处理测试资源文件至测试目标目录
test-compile|编译测试源码至测试目标目录
test|使用合适的单元测试框架运行测试。这些测试应该不需要代码被打包或发布
prepare-package|在真正的打包之前，执行一些准备打包必要的操作。这通常会产生一个包的展开的处理过的版本（将会在Maven 2.1+中实现）
package|将编译好的代码打包成可分发的格式，如JAR，WAR，或者EAR
pre-integration-test|执行一些在集成测试运行之前需要的动作。如建立集成测试需要的环境
integration-test|如果有必要的话，处理包并发布至集成测试可以运行的环境
post-integration-test|执行一些在集成测试运行之后需要的动作。如清理集成测试环境。
verify|执行所有检查，验证包是有效的，符合质量规范
install|安装包至本地仓库，以备本地的其它项目作为依赖使用
deploy|复制最终的包至远程仓库，共享给其它开发人员和项目（通常和一次正式的发布相关）

maven核心的插件列表可以参考 http://maven.apache.org/plugins/index.html 。这里仅列举几个常用的插件及其配置参数：

clean插件：

只包含一个goal叫做 clean:clean ，负责清理构建时候创建的文件。 默认清理的位置是如下几个变量指定的路径 project.build.directory, project.build.outputDirectory, project.build.testOutputDirectory, and project.reporting.outputDirectory 。 

compiler插件：

包含2个goal，分别是 compiler:compile 和 compiler:testCompile 。可以到这里查看两者的具体参数设置：compile , testCompile 。 

surefire插件：

运行单元测试用例的插件，并且能够生成报表。包含一个goal为 surefire:test 。主要参数testSourceDirectory用来指定测试用例目录，参考完整用法帮助 

jar：

负责将工程输出打包到jar文件中。包含两个goal，分别是 jar:jar , jar:test-jar 。两个goal负责从classesDirectory或testClassesDirectory中获取所有资源，然后输出jar文件到outputDirectory中。 

war：

负责打包成war文件。常用goal有 war:war ，负责从warSourceDirectory（默认${basedir}/src/main/webapp）打包所有资源到outputDirectory中。 

resources：

负责复制各种资源文件，常用goal有 resources:resources ，负责将资源文件复制到outputDirectory中，默认为${project.build.outputDirectory}。 

install：

负责将项目输出(install:install)或者某个指定的文件(install:install-file)加入到本机库%USERPROFILE%/.m2/repository中。可以用 install:help 寻求帮助。 

deploy：

负责将项目输出(deploy:deploy)或者某个指定的文件(deploy:deploy-file)加入到公司库中。 

site：

将工程所有文档生成网站，生成的网站界面默认和apache的项目站点类似，但是其文档用doxia格式写的，目前不支持docbook，需要用其他插件配合才能支持。需要指出的是，在maven 2.x系列中和maven3.x的site命令处理是不同的，在旧版本中，用 mvn site 命令可以生成reporting节点中的所有报表，但是在maven3中，reporting过时了，要把这些内容作为 maven-site-plugin的configuration的内容才行。详细内容可以参考http://www.wakaleo.com/blog/292-site-generation-in-maven-3 
