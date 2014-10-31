# Waveform的安装与分析音频波形

## Step 1 源码获取

[github benalavi/ waveform](https://github.com/benalavi/waveform) 查看源码

## Step 2 安装

- 安装libsndfile：

    ```bash
    sudo apt-get install libsndfile1-dev
    ```

- 安装waveform，如果有代理打开代理，如果安装遇到‘treat wwarning as error’，打开后面的内容

    ```bash
    sudo gem [--http-proxy (http://usrname:passwd@proxy.xxx.com:8000)] waveform [ -- --with-cflags=-Wno-error=format-security]
    ```

- 运行命令，即可得到音频波形
    
    ```bash
    waveform song.wav waveform.png
    ```
