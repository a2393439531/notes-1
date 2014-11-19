# 综述

Python 这门解释性语言也有专门的线程模型，Python虚拟机使用GIL（Global Interpreter Lock，全局解释器锁）来互斥线程对共享资源的访问，但暂时无法利用多处理器的优势。

在Python中我们主要是通过 thread 和 threading 这两个模块来实现的，其中 Python 的threading 模块是对 thread 做了一些包装的，可以更加方便的被使用，所以我们使用 threading 模块实现多线程编程。这篇文章我们主要来看看Python对多线程编程的支持。

在语言层面，Python 对多线程提供了很好的支持，可以方便地支持创建线程、互斥锁、信号量、同步等特性。下面就是官网上介绍 Python3.4 threading 模块的基本资料及功能：

## 实现模块

- thread：多线程的底层支持模块，一般不建议使用；
- threading：对thread进行了封装，将一些线程的操作对象化

### threading 模块

主要类：

- Thread 线程类，这是我们用的最多的一个类，你可以指定线程函数执行或者继承自它都可以实现子线程功能；
- Timer 与 Thread 类似，但要等待一段时间后才开始运行
- Lock 锁原语，这个我们可以对全局变量互斥时使用；
- RLock 可重入锁，使单线程可以再次获得已经获得的锁；
- Condition 条件变量，能让一个线程停下来，等待其他线程满足某个“条件”；
- Event 通用的条件变量。多个线程可以等待某个事件发生，在事件发生后，所有的线程都被激活；
- Semaphore 为等待锁的线程提供一个类似“等候室”的结构；
- BoundedSemaphore 与semaphore类似，但不允许超过初始值；
- Queue：实现了多生产者（Producer）、多消费者（Consumer）的队列，支持锁原语，能够在多个线程之间提供很好的同步支持。

主要函数：

- active_count()
- current_thread()
- get_ident()
- enumerate()
- settrace(func)
- setprofile(func)
- stack_size([size])
- threading.TIMEOUT_MAX
- threading.local()

### Thread 类

函数原型：

```python
class threading.Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)
```

主要的线程类，可以创建进程实例。该类提供的函数包括：

- getName() 返回线程的名字。
- is_alive() 布尔标志，表示这个线程是否还在运行中。
- isDaemon() 返回线程的daemon标志。
- join(timeout=None) 程序挂起，直到线程结束，如果给出timeout，则最多阻塞timeout秒。
- run() 定义线程的功能函数。
- setDaemon(daemonic) 把线程的daemon标志设为daemonic。
- setName(name) 设置线程的名字。
- start() 开始线程执行。

### Queue 提供的类

- Queue队列
- LifoQueue后入先出（LIFO）队列
- PriorityQueue 优先队列

接下来，我们将会用一个一个示例来展示threading的各个功能，包括但不限于：两种方式起线程、threading.Thread类的重要函数、使用Lock互斥及RLock实现重入锁、使用Condition实现生产者和消费者模型、使用Event和Semaphore多线程通信。

# 两种方式起线程

在Python中我们主要是通过thread和threading这两个模块来实现的，其中Python的threading模块是对thread做了一些包装的，可以更加方便的被使用，所以我们使用threading模块实现多线程编程。一般来说，使用线程有两种模式，一种是创建线程要执行的函数，把这个函数传递进Thread对象里，让它来执行；另一种是直接从Thread继承，创建一个新的class，把线程执行的代码放到这个新的 class里。

## 将函数传递进 Thread 对象

```python
import threading

def thread_fun(num):
    for i in range(int(num)):
        print(threading.currentThread().getName(), 'num:', i)

def main(thread_num):
    thread_list = []

    # 创建线程对象
    for i in range(thread_num):
        thread_name = 'thread_%s' %i
        thread_list.append(threading.Thread(target = thread_fun, name = thread_name, args = (10,)))

    # 启动所有线程
    for thread in thread_list:
        thread.start()

    # 主线程中等待所有子线程退出
    for thread in thread_list:
        thread.join()

if __name__ == "__main__":
    main(3)
```

## 继承自 threading.Thread 类：

```python
import threading

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('Thread name %s' %self.name)


if __name__ == "__main__":
    for thread in range(0, 5):
        t = MyThread()
        t.start()
```

------

接下来，将会介绍如何控制这些线程，包括子线程的退出，子线程是否存活及将子线程设置为守护线程(Daemon)。

# threading.Thread 类的重要函数

## 1、name 相关

可以为每一个thread指定name，默认的是Thread-No形式的，如上述实例代码打印出的一样：

```
Thread name Thread-1
Thread name Thread-2
Thread name Thread-3
Thread name Thread-4
Thread name Thread-5
```

当然可以用 setName() 方法指定线程名，如下：

```python
    def __init__(self):
        threading.Thread.__init__(self)
        self.setName('My' + self.name)
```

## 2、join 方法

join方法原型如下，这个方法是用来阻塞当前上下文，直至该线程运行结束：

```python
def join(self, timeout=None):
```

timeout 可以设置超时时间

## 3、setDaemon 方法

当我们在程序运行中，执行一个主线程，如果主线程又创建一个子线程，主线程和子线程就分兵两路，当主线程完成想退出时，会检验子线程是否完成。如果子线程未完成，则主线程会等待子线程完成后再退出。但是有时候我们需要的是，只要主线程完成了，不管子线程是否完成，都要和主线程一起退出，这时就可以用setDaemon方法，并设置其参数为True。

# 使用 Lock 互斥锁

现在我们考虑这样一个问题：假设各个线程需要访问同一公共资源，我们的代码该怎么写？

```python
import threading
import time

counter = 0

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global counter
        time.sleep(1)
        counter += 1
        print('%s, set counter: %s' %(self.name, counter))

if __name__ == "__main__":
    for i in range(200):
        my_thread = MyThread()
        my_thread.start()
```

解决上面的问题，我们兴许会写出这样的代码，我们假设跑200个线程，但是这200个线程都会去访问counter这个公共资源，并对该资源进行处理(counter += 1)，代码看起来就是这个样了，但是我们看下运行结果（Python2.7）：

*注：在Python3.4中没有如下争抢的情况*

```
Thread-119, set counter: 108
 Thread-130, set counter: 143
Thread-124, set counter: 127
Thread-125, set counter: 112Thread-143, set counter: 130
Thread-154, set counter: 145
 Thread-150, set counter: 131
Thread-144, set counter: 146

```

打印结果我只贴了一部分，从中我们已经看出了这个全局资源(counter)被抢占的情况，问题产生的原因就是没有控制多个线程对同一资源的访问，对数据造成破坏，使得线程运行的结果不可预期。这种现象称为“线程不安全”。在开发过程中我们必须要避免这种情况，那怎么避免？这就用到了我们在综述中提到的互斥锁了。

## 互斥锁概念

Python编程中，引入了对象互斥锁的概念，来保证共享数据操作的完整性。每个对象都对应于一个可称为” 互斥锁” 的标记，这个标记用来保证在任一时刻，只能有一个线程访问该对象。在Python中我们使用threading模块提供的Lock类。

我们对上面的程序进行整改，为此我们需要添加一个互斥锁变量 `mutex = threading.Lock()`，然后在争夺资源的时候之前我们会先抢占这把锁 `mutex.acquire()`，对资源使用完成之后我们在释放这把锁 `mutex.release()`。代码如下：

```python
import threading
import time

counter = 0
mutex = threading.Lock()

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global counter
        time.sleep(1)
        if mutex.acquire():
            counter += 1
            print('%s, set counter: %s' %(self.name, counter))
            mutex.release()

if __name__ == "__main__":
    for i in range(200):
        my_thread = MyThread()
        my_thread.start()
```

## 同步阻塞

当一个线程调用Lock对象的acquire()方法获得锁时，这把锁就进入“locked”状态。因为每次只有一个线程1可以获得锁，所以如果此时另一个线程2试图获得这个锁，该线程2就会变为“block“同步阻塞状态。直到拥有锁的线程1调用锁的release()方法释放锁之后，该锁进入“unlocked”状态。线程调度程序从处于同步阻塞状态的线程中选择一个来获得锁，并使得该线程进入运行（running）状态。

**进一步考虑**

通过对公共资源使用互斥锁，这样就简单的到达了我们的目的，但是如果我们又遇到下面的情况：

1. 遇到锁嵌套的情况该怎么办，这个嵌套是指当我一个线程在获取临界资源时，又需要再次获取；
2. 如果有多个公共资源，在线程间共享多个资源的时候，如果两个线程分别占有一部分资源并且同时等待对方的资源；

上述这两种情况会直接造成程序挂起，即死锁，下面我们会谈死锁及可重入锁RLock。

# 死锁的形成

现在考虑下面的情况：如果有多个公共资源，在线程间共享多个资源的时候，如果两个线程分别占有一部分资源并且同时等待对方的资源，这会引起什么问题？

## 死锁的概念

所谓死锁： 是指两个或两个以上的进程在执行过程中，因争夺资源而造成的一种互相等待的现象，若无外力作用，它们都将无法推进下去。此时称系统处于死锁状态或系统产生了死锁，这些永远在互相等待的进程称为死锁进程。 由于资源占用是互斥的，当某个进程提出申请资源后，使得有关进程在无外力协助下，永远分配不到必需的资源而无法继续运行，这就产生了一种特殊现象死锁。

```python
import threading

counterA = 0
counterB = 0

mutexA = threading.Lock()
mutexB = threading.Lock()

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        self.func1()
        self.func2()

    def func1(self):
        global mutexA, mutexB
        if mutexA.acquire():
            print('%s, get res: %s' %(self.name, "ResA"))
            if mutexB.acquire():
                print('%s, get res: %s' %(self.name, "ResB"))
                mutexB.release()
            mutexA.release()

    def func2(self):
        global mutexA, mutexB
        if mutexB.acquire():
            print('%s, get res: %s' %(self.name, "ResB"))
            if mutexA.acquire():
                print('%s, get res: %s' %(self.name, "ResA"))
                mutexA.release()
            mutexB.release()

if __name__ == "__main__":
    for i in range(10):
        tmpthread = MyThread()
        tmpthread.start()
```

代码中展示了一个线程的两个功能函数分别在获取了一个竞争资源之后再次获取另外的竞争资源，我们看运行结果：

```
Thread-7, get res: ResB
Thread-7, get res: ResA
Thread-8, get res: ResA
Thread-8, get res: ResB
Thread-9, get res: ResA
Thread-8, get res: ResB
```

可以看到，程序已经挂起在那儿了，这种现象我们就称之为”死锁“。

## 避免死锁

避免死锁主要方法就是：正确有序的分配资源，避免死锁算法中最有代表性的算法是Dijkstra E.W 于1968年提出的银行家算法。

# 可重入锁RLock

考虑这种情况：如果一个线程遇到锁嵌套的情况该怎么办，这个嵌套是指当我一个线程在获取临界资源时，又需要再次获取。

根据这种情况，代码如下：

```python
import threading
import time
 
counter = 0
mutex = threading.Lock()
 
class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
 
    def run(self):
        global counter, mutex
        time.sleep(1);
        if mutex.acquire():
            counter += 1
            print("%s, set counter:%s" % (self.name, counter))
            if mutex.acquire():
                counter += 1
                print("%s, set counter:%s" % (self.name, counter))
                mutex.release()
            mutex.release()
 
if __name__ == "__main__":
    for i in range(10):
        my_thread = MyThread()
        my_thread.start()
```

这种情况的代码运行情况如下：

```
Thread-1, set counter:1
```

之后就直接挂起了，这种情况形成了最简单的死锁。

那有没有一种情况可以在某一个线程使用互斥锁访问某一个竞争资源时，可以再次获取呢？在Python中为了支持在同一线程中多次请求同一资源，python提供了“可重入锁”：threading.RLock。这个RLock内部维护着一个Lock和一个counter变量，counter记录了acquire的次数，从而使得资源可以被多次require。直到一个线程所有的acquire都被release，其他的线程才能获得资源。上面的例子如果使用RLock代替Lock，则不会发生死锁：

**代码只需将上述的：**

```python
mutex = threading.Lock()
```

替换为：

```python
mutex = threading.RLock()
```

# 使用Condition实现复杂同步

目前我们已经会使用Lock去对公共资源进行互斥访问了，也探讨了同一线程可以使用RLock去重入锁，但是尽管如此我们只不过才处理了一些程序中简单的同步现象，我们甚至还不能很合理的去解决使用Lock锁带来的死锁问题。所以我们得学会使用更深层的解决同步问题。

Python提供的Condition对象提供了对复杂线程同步问题的支持。Condition被称为条件变量，除了提供与Lock类似的acquire和release方法外，还提供了wait和notify方法。

使用Condition的主要方式为：线程首先acquire一个条件变量，然后判断一些条件。如果条件不满足则wait；如果条件满足，进行一些处理改变条件后，通过notify方法通知其他线程，其他处于wait状态的线程接到通知后会重新判断条件。不断的重复这一过程，从而解决复杂的同步问题。

下面我们通过很著名的“生产者-消费者”模型来来演示下，在Python中使用Condition实现复杂同步。

```python
import threading
import time

condition = threading.Condition()
products = 0

class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global condition, products
        while True:
            if condition.acquire():
                if products < 10:
                    products += 1
                    print('Producer(%s): deliver one, now products: %s' %(self.name, products))
                    condition.notify()
                else:
                    print('Producer(%s): already 10, stop deliver, now products: %s' %(self.name, products))

                condition.release()
                time.sleep(2)

class Consumer(threading.Thread):
    """docstring for Consumer"""
    def __init__(self):
        super(Consumer, self).__init__()

    def run(self):
        global condition, products
        while True:
            if condition.acquire():
                if products > 1:
                    products -= 1
                    print('Consumer(%s): consume one, now products: %s' %(self.name, products))
                    condition.notify()
                else:
                    print('Consumer(%s): only 1, stop consume, products: %s' %(self.name, products))
                    condition.wait()
                condition.release()
                time.sleep(2)

if __name__ == "__main__":
    for i in range(2):
        p = Producer()
        p.start()

    for i in range(10):
        c = Consumer()
        c.start()
```

代码中主要实现了生产者和消费者线程，双方将会围绕products来产生同步问题，首先是2个生成者生产products ，而接下来的10个消费者将会消耗products，代码运行如下：

```
Producer(Thread-1):deliver one, now products:1
Producer(Thread-2):deliver one, now products:2
Consumer(Thread-3):consume one, now products:1
Consumer(Thread-4):only 1, stop consume, products:1
Consumer(Thread-5):only 1, stop consume, products:1
Consumer(Thread-6):only 1, stop consume, products:1
Consumer(Thread-7):only 1, stop consume, products:1
Consumer(Thread-8):only 1, stop consume, products:1
Consumer(Thread-10):only 1, stop consume, products:1
Consumer(Thread-9):only 1, stop consume, products:1
Consumer(Thread-12):only 1, stop consume, products:1
Consumer(Thread-11):only 1, stop consume, products:1
```

另外：Condition对象的构造函数可以接受一个Lock/RLock对象作为参数，如果没有指定，则Condition对象会在内部自行创建一个RLock；除了notify方法外，Condition对象还提供了notifyAll方法，可以通知waiting池中的所有线程尝试acquire内部锁。由于上述机制，处于waiting状态的线程只能通过notify方法唤醒，所以notifyAll的作用在于防止有线程永远处于沉默状态。

# 使用Event实现线程间通信

使用threading.Event可以实现线程间相互通信，之前的Python：使用threading模块实现多线程编程七[使用Condition实现复杂同步]我们已经初步实现了线程间通信的基本功能，但是更为通用的一种做法是使用threading.Event对象。

使用threading.Event可以使一个线程等待其他线程的通知，我们把这个Event传递到线程对象中，Event默认内置了一个标志，初始值为False。一旦该线程通过wait()方法进入等待状态，直到另一个线程调用该Event的set()方法将内置标志设置为True时，该Event会通知所有等待状态的线程恢复运行。

```python
import threading
import time

class MyThread(threading.Thread):
    def __init__(self, singal):
        super(MyThread, self).__init__()
        self.singal = singal

    def run(self):
        print('%s, will sleep...' %self.name)
        self.singal.wait()
        print('%s, awake...' %self.name)

if __name__ == "__main__":
    singal = threading.Event()
    for t in range(3):
        thread = MyThread(singal)
        thread.start()

    print('main thread sleep 3 seconds...')
    time.sleep(3)

    singal.set()
```

运行效果如下：

```
Thread-1, will sleep...
Thread-2, will sleep...
Thread-3, will sleep...
main thread sleep 3 seconds...
Thread-1, awake...
Thread-2, awake...
Thread-3, awake...
```

来自：http://www.ourunix.org/
