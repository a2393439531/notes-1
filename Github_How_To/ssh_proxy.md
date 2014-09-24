# github ssh proxy协议代理配置

公司使用代理，github不能使用ssh管理git仓库，只能通过https由用户名密码登陆，网搜了一下发现了两个方法，过程相似。但是使用nc命令的方法一没有运行成功，因为对该命令不熟，没有深究，改用方法二成功。

一般通过http代理，只能访问外网的443和80端口，github现在本身就支持https的方式提交代码，这里讲的是如何通过默认方式即git协议提交代码，我们知道git是基于ssh的，端口是22，github这个服务器的ssh端口我们又不能像自己的服务器一样改成443，怎么办呢。在基于http做好的ssh代理之上，再连接github，已经开启的ssh代理是不受端口限制的。

## 方法一

配置一个 `proxy-wrapper` 脚本

```bash
cat > $HOME/bin/proxy-wrapper
#!/bin/bash
nc -x 127.0.0.1:7080 -X5 $*
```

给它增加一个可执行权限

```bash
$ chmod +x $HOME/bin/proxy-wrapper
```

配置 `.ssh/config` , 对 github.com 设置一个代理命令

```bash
Host github github.com
    Hostname github.com
    User git
    ProxyCommand $HOME/bin/proxy-wrapper '%h %p'
```

**必须全部走ssh协议**

```bash
$ git clone git@github.com:meshinestar/HelloGit.git
```

以上，参考：http://fengmk2.cnpmjs.org/github-proxy.html。

但是感觉这个方法不如这个详细：http://fungo.me/linux/tunneling-ssh-over-http-proxy.html，只是没有尝试。

------

## 方法二

配置 `.ssh/config` , 对 github.com 设置一个代理命令

```bash
Host github.com 
ProxyCommand ~/.ssh/ssh-https-tunnel %h %p ~/.ssh/proxyauth
Port 443
Hostname ssh.github.com
```

这里你可以看到第二行最后有一个`~/.ssh/proxyauth`。这是因为我单位的代理有口令，所以要再生成一个`proxyauth`文件，格式就是：`username:password`。如果你没有，去掉它就行了。

同时`Hostname`的目的是为了创建一个别名，其实我们使用的是`ssh.github.com`，但是因为平时都使用`git@github.com`，所以为了不进行修改，创建一个别名。

下载ssh-https-tunnel，可以从 http://zwitterion.org/software/ssh-https-tunnel/ssh-https-tunnel ，保存到你的git的~/.ssh目录下，同时要打开这个文件进行修改，将：

```perl
my $proxy = "";
my $proxy_port = ;
```
改成你的实际的代理服务器地址。

使用ssh git@github.com 来测试

```bash
The authenticity of host 'github.com (192.38.252.124)' can't be established.
RSA key fingerprint is 16:27:ac:a5:76:28:2d:36:63:1b:56:4d:eb:df:a6:48.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'github.com,192.38.252.124' (RSA) to the list of known hosts.
Permission denied (publickey).
```

以上，参考：http://blog.chinaunix.net/uid-22627501-id-3050090.html

