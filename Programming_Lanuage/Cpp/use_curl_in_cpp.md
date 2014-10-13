# C++怎么使用curl发送http请求？

## Step 1：安装libcurl

先下载并安装libcurl，目前版本是7.38.0. 官方地址：http://curl.haxx.se/

下载源码后，看ReadMe，如果没有特殊编译需求，直接：

1. ./configure
2. make
3. (sudo) make install

安装完成。

## Step 2：安装curlcpp

github地址：https://github.com/JosephP91/curlcpp

下载源码后，看ReadMe，直接：

1. cd build
2. cmake ..
3. make

然后，把编译出的libcurlcpp.a和include文件夹下的.h文件放到/usr/local下，或者在工程中引入即可。

## Step 3：如何使用

*例一：使用curl_easy接口发送HTTP request*

```cpp
#include "curl_easy.h"

using curl::curl_easy;

int main(int argc, const char **argv) {
    curl_easy easy;
    easy.add(curl_pair<CURLoption,string>(CURLOPT_URL,"http://www.google.it") );
    easy.add(curl_pair<CURLoption,long>(CURLOPT_FOLLOWLOCATION,1L));
    try {
        easy.perform();
    } catch (curl_easy_exception error) {
        // If you want to get the entire error stack we can do:
        vector<pair<string,string>> errors = error.what();
        // Otherwise we could print the stack like this:
        error.print_traceback();
        // Note that the printing the stack will erase it
    }
    return 0;
}
```


*例二：使用curl_easy接口进行HTTPS POST登陆*

```cpp
#include "curl_easy.h"
#include "curl_form.h"

using curl::curl_form;
using curl::curl_easy;

int main(int argc, const char * argv[]) {
    curl_form form;
    curl_easy easy;

    // Forms creation
    curl_pair<CURLformoption,string> name_form(CURLFORM_COPYNAME,"user");
    curl_pair<CURLformoption,string> name_cont(CURLFORM_COPYCONTENTS,"you username here");
    curl_pair<CURLformoption,string> pass_form(CURLFORM_COPYNAME,"passw");
    curl_pair<CURLformoption,string> pass_cont(CURLFORM_COPYCONTENTS,"your password here");

    try {
        // Form adding
        form.add(name_form,name_cont);
        form.add(pass_form,pass_cont);

        // Add some options to our request
        easy.add(curl_pair<CURLoption,string>(CURLOPT_URL,"your url here"));
        easy.add(curl_pair<CURLoption,bool>(CURLOPT_SSL_VERIFYPEER,false));
        easy.add(curl_pair<CURLoption,curl_form>(CURLOPT_HTTPPOST,form));
        easy.perform();
    } catch (curl_easy_exception error) {
        // Print errors, if any
        error.print_traceback();
    }
    return 0;
}
```

*例三：内容以文件形式返回，非常简单可以做到*

```cpp
#include <iostream>
#include "curl_easy.h"
#include <fstream>

using std::cout;
using std::endl;
using std::ofstream;
using curl::curl_easy;

int main(int argc, const char * argv[]) {
    // Create a file
    ofstream myfile;
    myfile.open ("/Users/Giuseppe/Desktop/test.txt");
    // Create a writer to handle the stream

    curl_writer writer(myfile);
    // Pass it to the easy constructor and watch the content returned in that file!
    curl_easy easy(writer);

    // Add some option to the easy handle
    easy.add(curl_pair<CURLoption,string>(CURLOPT_URL,"http://www.google.it") );
    easy.add(curl_pair<CURLoption,long>(CURLOPT_FOLLOWLOCATION,1L));
    try {
        easy.perform();
    } catch (curl_easy_exception error) {
        // If you want to get the entire error stack we can do:
        vector<pair<string,string>> errors = error.what();
        // Otherwise we could print the stack like this:
        error.print_traceback();
    }
    myfile.close();
    return 0;
}
```

作者实现了一个sender和一个receiver，这样在使用send/receive的时候无需再持有buffer，send/receive也如此简单：

*例四：send/receive*

```cpp
#include "curl_easy.h"
#include "curl_form.h"
#include "curl_pair.h"
#include "curl_receiver.h"
#include "curl_sender.h"

using curl::curl_form;
using curl::curl_easy;
using curl::curl_sender;
using curl::curl_receiver;

int main(int argc, const char * argv[]) {
    // Simple request
    string request = "GET / HTTP/1.0\r\nHost: example.com\r\n\r\n";

    // Creation of easy object.
    curl_easy easy;
    try {
        easy.add(curl_pair<CURLoption,string>(CURLOPT_URL,"http://example.com"));
        // Just connect
        easy.add(curl_pair<CURLoption,bool>(CURLOPT_CONNECT_ONLY,true));
        easy.perform();
    } catch (curl_easy_exception error) {
        // If you want to get the entire error stack we can do:
        vector<pair<string,string>> errors = error.what();
        // Print errors if any
        error.print_traceback();
    }

    // Creation of a sender. You should wait here using select to check if socket is ready to send.
    curl_sender<string> sender(easy);
    sender.send(request);
    // Prints che sent bytes number.
    cout<<"Sent bytes: "<<sender.get_sent_bytes()<<endl;

    for(;;) {
        // You should wait here to check if socket is ready to receive
        try {
            // Create a receiver
            curl_receiver<char,1024> receiver;
            // Receive the content on the easy handler
            receiver.receive(easy);
            // Prints the received bytes number.
            cout<<"Receiver bytes: "<<receiver.get_received_bytes()<<endl;
        } catch (curl_easy_exception error) {
            // If any errors occurs, exit from the loop
            break;
        }
    }
    return 0;
}
```
