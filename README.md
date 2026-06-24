# hoyoLancherWPDL
下载米哈游启动器的背景动态壁纸的一个简单的python脚本

## 使用方法
1. 确保你已经安装了pyhton
2. 下载了.py文件后在文件保存的地方打开终端, 运行 `python wallpaperDownload.py`命令
3. 下载好的文件会在media文件夹里

文件结构:
```ascill
\图片\WALLPAPERDOWNLOAD
|   wallpaperDownload.py
|
\---media
    |   1.webm
    |   10.webm
    |   11.webm
    |   2.webm
    |   3.webm
    |   4.webm
    |   5.webm
    |   6.webm
    |   7.webm
    |   8.webm
    |   9.webm
    |
    \---cache
            downloaded_links.txt
```
cache里的.txt文件是用来记录已经下载过的文件链接的, 并不使用MD5区分下载文件是否重复, 仅在下载时就链接简单判断
