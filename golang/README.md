### 武汉肺炎病患数据的  golang  Bitbar 插件



![enter description here][1]
#### 前提
- macOS
- 安装了 [Bitbar](https://getbitbar.com)


#### 如何安装插件
- 在电脑上打开 Bitbar，把本 repo 里的 `go-plugin` 放入 Bitbar 指定的插件文件夹中
- 在状态栏中选中 Bitbar 的图标，点击刷新即可

---

#### Q&A

**数据源是哪里来的？**
- 来自丁香园的网页，插件每 10s 会刷新一次，去抓取丁香园网页的数据。丁香园的数据也会有一些延迟，但还是比较可靠的。



  [1]: https://demonsec666.oss-cn-qingdao.aliyuncs.com/1580304645387.jpg 