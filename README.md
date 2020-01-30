### 武汉肺炎病患数据的 Bitbar 插件

<img src="https://sm.ms/image/WKtxIhVFrM5swyT" alt="长这样" width="500">

#### 前提
- macOS
- 安装了 [Bitbar](https://getbitbar.com)
- 安装了 nodejs，并且 `yarn add global request`

#### 如何安装插件
- 在电脑上打开 Bitbar，把本 repo 里的 `wuhan.10s.js` 放入 Bitbar 指定的插件文件夹中(新建文件夹即可)
- 在状态栏中选中 Bitbar 的图标，点击刷新即可

---

#### 一些客制化的小功能

**刷新时间**
- 默认是 10 秒刷新一次。如果想修改成 1 小时刷新一次，把文件名中 `wuhan.10s.js` 改成 `wuhan.1h.js` 即可。

**展示的省份**
- 默认展示确认患病人数最多的五个省份
- 可以打开 `wuhan.10s.js`，在 `targetProvinceName` 中填入你想看的省份的名字

---

#### Q&A

**数据源是哪里来的？**
- 来自丁香园的网页，插件每 10s 会刷新一次，去抓取丁香园网页的数据。丁香园的数据也会有一些延迟，但还是比较可靠的。

**为什么我的电脑上看不到数据？**
- node环境缺少
- request依赖缺失
- 全局代理ip可能导致获取不到数据
