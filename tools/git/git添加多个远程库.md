## 使用流程

首先，我们从零开始， 
假设你现在想要增加3个远程库地址，分别为 :

- https://git.oschina.net/shede333/swioslibary.git 
- https://git.oschina.net/shede333/swscrollbar.git 
- https://github.com/shede333/CoreAnimationTestSW.git

首先，先增加第一个地址 `git remote add origin <url1> `
然后增加第二个地址 `git remote set-url --add origin <url2> `
增加第三个地址 `git remote set-url --add origin <url3> `
….依次类推

这样就完成了添加多个地址到origin库中了， 

以后只要使用git push origin master 就可以一次性push到3各库里面了(使用git push也可)
