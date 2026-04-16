# 📚Mastodon 嘟文迁移至 Wordpress 完整指引

本指引教程包含：

* 🐘Mastodon 的数据导出
* 🛠️WordPress 的设置与主题安装
* 🪄媒体的导入与 JSON 导入插件的使用

---

## 🐘Mastodon 数据导出

首先需要从 Mastodon 导出嘟文和媒体的存档  
在 Mastodon 的**设置**→**导出**界面，点击**请求你的存档**

![请求Mastodon存档](../images/guide/md-export-step1.jpg)

请求存档需要一点时间，等存档准备好后就下载你的存档

![下载Mastodon存档](../images/guide/md-export-step2.jpg)

下载后你会得到如下的文件  
`media_attachments`里面存放着图片和视频等媒体文件  
`outbox.json`记录着所有的嘟文

![存档文件结构](../images/guide/md-export-step3.jpg)


---

## 🛠️WordPress 的设置与主题安装

下面进行 WordPress 的设置（WordPress 的部署不在本教程范围内）  
这里以一个新部署好的 WordPress6.9 网站为例  
进入网站的后台页面

![WordPress6.9](../images/guide/wp-import-step1.jpg)

第一步，先安装导入嘟文必须用到的插件**Post Export Import with Media**  
在 WordPress 左边栏找到**插件**→**安装插件**  
搜索找到**Post Export Import with Media**，立刻安装并启用

![安装插件](../images/guide/wp-import-step2.jpg)

第二步，安装本项目准备好的主题文件  
（会装修 WordPress 的可以省略这步，这里仅为方便想快速看到整体博客效果的人）

先下载主题文件 [mastodon.zip](https://github.com/kunsui/mastodon_to_wordpress/raw/refs/heads/main/theme/mastodon.zip)

```
theme/mastodon.zip
```

在 WordPress 左边栏找到**外观**→**主题**→**安装主题**  
然后上传安装刚才下载好的主题文件`mastodon.zip`

![上传安装主题文件](../images/guide/wp-import-step3.jpg)

安装完成后回到主题界面，启用刚才安装的主题**Mastodon**

![启用主题文件](../images/guide/wp-import-step4.jpg)

第三步，还有几个小设置需要设定一下  
在 WordPress 左边栏找到**设置**→**阅读**  
**博客页面至多显示**这一项，建议设置为**50**以上

![设置博客页面至多显示](../images/guide/wp-import-step5.jpg)

继续在左边栏找到**设置**→**固定链接**  
**固定链接结构**这一项，建议设置为**朴素**

![设置固定链接结构](../images/guide/wp-import-step6.jpg)

以上，WordPress 的基本设置就结束了  
可以点击左上角的站点名称去到站点首页，查看当前的首页，大概是如下的样子

![站点首页](../images/guide/wp-import-step7.jpg)

<img src="../images/video.png" alt="视频图标" width="200">

