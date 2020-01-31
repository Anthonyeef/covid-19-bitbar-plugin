## 武汉肺炎病患数据的 Bitbar 插件

<img src="https://tva1.sinaimg.cn/large/006tNbRwly1gbchjabjxrj30si0pu1kx.jpg" alt="长这样" width="500">

### 前提
- macOS
- 安装了 [Bitbar](https://getbitbar.com)
- 安装了 Python 3.x，并且 `pip install requests`

### 如何安装插件
- 在电脑上打开 Bitbar，把本 repo 里的 `wuhan.10s.py` 放入 Bitbar 指定的插件文件夹中
- 在状态栏中选中 Bitbar 的图标，点击刷新即可

---

### 一些客制化的小功能

**刷新时间**
- 默认是 10 秒刷新一次。如果想修改成 1 小时刷新一次，把文件名中 `wuhan.10s.py` 改成 `wuhan.1h.py` 即可。

**展示的省份**
- 默认展示确认患病人数最多的五个省份
- 可以打开 `wuhan.10s.py`，在 `targetProvinceName` 中填入你想看的省份的名字
- 除了默认展示的五个省份外，还可以在 `additionProvinceName` 中填入想额外关注的省份的名字

---

### 其他语言的实现
- 发布后陆续收到了一些热心网友的 PR，也一并列举在下： 
    - [Javascript 版](https://github.com/Anthonyeef/wuhan-virus-bitbar-plugin/pull/7)
    - [Go 版](https://github.com/Anthonyeef/wuhan-virus-bitbar-plugin/pull/5)

### Q&A

**数据源是哪里来的？**
- 来自丁香园的网页，插件每 10s 会刷新一次，去抓取丁香园网页的数据。丁香园的数据也会有一些延迟，但还是比较可靠的。

**为什么我的电脑上看不到数据？**
- 需要确保自己电脑上是 Python 3.x 
- 把自己电脑上 Python 3.x 的路径替换掉 `wuhan.10.py` 开头的那一行 `#!/usr/local/bin/python3`
- 脚本依赖 requests 模块，需要在终端中 `pip install requests`。如果是 macOS 预装的 Python 2.7，可能 pip 也不是和 Python 3.x 对应的 pip，需要确认好

**我也想提交其他语言的版本**
- 可以新提一个 PR，放入到新增的 `other-languages` 目录下
- 注意：需要提交脚本 + 安装说明(简单的 README)