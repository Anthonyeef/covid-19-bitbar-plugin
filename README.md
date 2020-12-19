## 此fork与原版的不同
增加了全球、其他国家、现存数量、每日增减的数据。国内后疫情时代，我们更希望关注的大多是世界疫情。

PR其实发了，但是原作者迟迟不merge，故自己写了。希望原作者如果看到请merge一下～

## 新冠病患数据的 Bitbar 插件

<img src="https://github.com/SkyYkb/covid-19-bitbar-plugin/raw/master/screenshot.png" alt="长这样" width="500">

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
    - [Javascript 版](https://github.com/ChenYCL/wuhan-virus-bitbar-plugin)
    - [Go 版](https://github.com/Anthonyeef/wuhan-virus-bitbar-plugin/pull/5)

### Q&A

**数据源是哪里来的？**
- 最开始来自丁香园的网页；现在的版本使用了新浪的接口。每 10s 刷新一次。

**全国的数据为什么跟其他平台不大一致？**
- 新浪的接口会返回一个来自国家卫健委统计的全国数据，但这个数据变化不那么频繁，一天更新一次。
- 各省份的数据会稍微更新更加及时一些。
- 展示的策略是这样：先优先展示卫健委的全国数据。同时也会计算各省份的数据，如果加和超过了卫健委的数据，说明是各省份的数据更 `新鲜` 一些了。此时用各省份加和拿到的数据来做全国数据的展示。
- 这也和丁香园的策略大体保持一致。可以见 https://github.com/Anthonyeef/wuhan-virus-bitbar-plugin/issues/13 的讨论。

**为什么我的电脑上看不到数据？**
- 需要确保自己电脑上是 Python 3.x 
- 把自己电脑上 Python 3.x 的路径替换掉 `wuhan.10.py` 开头的那一行 `#!/usr/local/bin/python3`
- 脚本依赖 requests 模块，需要在终端中 `pip install requests`。如果是 macOS 预装的 Python 2.7，可能 pip 也不是和 Python 3.x 对应的 pip，需要确认好

**我也想提交其他语言的版本**
- 可以新提一个 PR，放入到新增的 `other-languages` 目录下
- 注意：需要提交脚本 + 安装说明(简单的 README)

**我想了解多一些类似的插件**
- 可以查看少数派的这篇[文章](https://sspai.com/post/58683)
