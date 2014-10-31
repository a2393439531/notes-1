# svn checkout 部分目录

## 问题

假如有一个svn仓库：http://localhost:8081/svn/HelloFruits/，里面有Trunk/Apple/，Trunk/Pear/，Trunk/Orange/目录，而你只想检出Apple目录，如何做呢？

## 解决方法

```bash
$ svn checkout --non-recrsive http://localhost:8081/svn/HelloFruits/
$ cd HelloFruits/
$ svn update --set-depth infinity Trunk/Apple/
```
