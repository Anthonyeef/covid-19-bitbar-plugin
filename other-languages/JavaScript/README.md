js版本切换

### 武汉肺炎病患数据的 Bitbar 插件

<img src="https://i.loli.net/2020/02/04/fJZU5cGgnj84QBv.png" alt="长这样" width="500">

#### 前提
- macOS
- 安装了 [Bitbar](https://getbitbar.com)
- 环境依赖 nodejs

#### 如何安装插件
- 在电脑上打开 Bitbar，下载文件，change plugin folder 为 wuhan文件夹
- 安装依赖，在wuhan-virus-bitbar-plugin 文件打开终端,  ```npm install```
- 在终端授权 chmod 777 wuhan.10s.js
- 在状态栏中选中 Bitbar 的图标，点击刷新即可

---

#### 爬虫版本额外配置
- 爬虫数据较准确，建议使用
- 配置
    ```JavaScript
        displayTop5ToRed: true,  // 默认显示前五省份红色 false关闭
        myFocusProvince: ['湖北'], // 关注省份 ["湖北","广东"] 添加多个
        focusProvinceColor:'blue', // 关注省份颜色
        myFocusCounty:['武汉'], // 额外关注城市 同省份配置
        focusCountyColor:'blue' // 关注城市颜色

    ```

#### 一些客制化的小功能

**刷新时间**
- 默认是 10 秒刷新一次。如果想修改成 1 小时刷新一次，把文件名中 `wuhan.10s.js` 改成 `wuhan.1h.js` 即可。

**展示的省份**
- 默认展示确认患病人数最多的五个省份
- 可以打开 `wuhan.10s.js`，在 `targetProvinceName` 中填入你想看的省份的名字

---

#### Q&A

**数据源是哪里来的？**
- 来自丁香园/新浪的网页，插件每 10s 会刷新一次，去抓取网页的数据。丁香园的数据也会有一些延迟，但还是比较可靠的。

**为什么我的电脑上看不到数据？**
- node环境缺少
- request依赖缺失
- 全局代理ip可能导致获取不到数据
