# 利用open命令在terminal中打开Finder

对于开发者来说，总是会在terminal和文件浏览器之间频繁切换，而对于Mac来说我还是小白，所以一些小技巧纪录一下，别忘了。

## 一、当前Finder中打开terminal

Mac OS X 10.10里面默认关闭了在Finder中打开terminal的服务，这样打开：

**System Preferences > Keyboard > Keyboard Shortcuts > Services**

选中复选框`New Terminal at Folder`，之后在文件夹上右键就可以在下面看到相应选项。

## 二、Terminal中打开当前Finder

只需要在terminal中，如下：

```sh
open .
```

另外open也可以打开任何文件（当然是以系统默认的应用程序打开）