# 问题

Solr server架设在CentOS上，使用Tomcat驱动，然而我写的Solr分词插件在我机器上好用但是在Solr Server上不好用？调查开始...

# 步骤

1. 登陆Server的Solr主页，查看Core配置，全无问题。
2. 在Analyze页面输入短句分词，立马TokenizerFactory.create异常，然后发现是版本问题。我用的是Solr4.9，CentOS上的是Solr4.8。
3. 修改插件的编辑环境为Solr4.8，编译打包，更换。本想一切OK，但是可爱的红色异常仍出现。
4. 发狠了，要来Server口令，ssh登陆后细细查看tomcat和solr的所有配置均无问题，有点想疯！
5. 再次发狠，比对4.8和4.9的apache doc中关于TokenizerFactory的所有接口，发现TokenizerFactory.create接口参数的命名空间果然不一样。
6. 修正接口，打包，上传，替换，重启tomcat，我靠，狗日的tomcat竟然不能工作了。
7. ps 查看进程发现有两个tomcat进程，全杀，再启动。
8. 哇哦，一切这么完美。^_^。

# 经验总结

1. 有句话叫“不怕狼一样的对手，就怕猪一样的队友”，我要说，切！千万别以为别人都想猪一样，尤其团队合作中，出问题必须先检查自己。
2. 干任何工作，尤其是建筑师、程序员千万不能急躁，屋子是一块砖一块砖砌的，代码是一行一行写的，每一行代码都得过一下大脑。

## 远程登陆linux主机

```sh
ssh -l usrname ip
# ssh -l root 192.168.2.1
```

## 远程Copy文件

```sh
scp /path/to/file usrname@ip.ip.ip.ip:/opt/
# scp hello.txt root@192.168.2.1:/opt/
```

## 查找并杀掉进程

```sh
ps -ef | grep tomcat

root   25893  1878  0 13:37 pts/10   00:00:34 xxxxx
```

杀掉

```sh
kill -s 9 25893
```

