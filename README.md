### 武汉肺炎病患数据的 Bitbar 插件

<img src="https://tva1.sinaimg.cn/large/006tNbRwly1gbchjabjxrj30si0pu1kx.jpg" alt="长这样" width="500">

#### 前提
- macOS
- 安装了 [Bitbar](https://getbitbar.com)
- 安装了 Python 3.x，并且 `pip install requests`

#### 如何安装插件
- 在电脑上打开 Bitbar，把本 repo 里的 `wuhan.10s.py` 放入 Bitbar 指定的插件文件夹中
- 在状态栏中选中 Bitbar 的图标，点击刷新即可

> 如果安装后未显示结果，且点击菜单栏图标后看到 ‘launch path not accessible’
>
> 请执行：
>
> `chmod +x wuhan.10s.py`
>
> 然后点击图标，再选择 Preferences > Refresh All

---

#### 一些客制化的小功能

**刷新时间**
- 默认是 10 秒刷新一次。如果想修改成 1 小时刷新一次，把文件名中 `wuhan.10s.py` 改成 `wuhan.1h.py` 即可。

**展示的省份**
- 默认展示确认患病人数最多的五个省份
- 可以打开 `wuhan.10s.py`，在 `targetProvinceName` 中填入你想看的省份的名字
- 除了默认展示的五个省份外，还可以在 `additionProvinceName` 中填入想额外关注的省份的名字

---

#### Q&A

**数据源是哪里来的？**
- 来自丁香园的网页，插件每 10s 会刷新一次，去抓取丁香园网页的数据。丁香园的数据也会有一些延迟，但还是比较可靠的。

**为什么我的电脑上看不到数据？**
- 需要确保自己电脑上是 Python 3.x 
- 把自己电脑上 Python 3.x 的路径替换掉 `wuhan.10.py` 开头的那一行 `#!/usr/local/bin/python3`
- 脚本依赖 requests 模块，需要在终端中 `pip install requests`。如果是 macOS 预装的 Python 2.7，可能 pip 也不是和 Python 3.x 对应的 pip，需要确认好
