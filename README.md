# 🐘 Mastodon → WordPress 迁移工具

将 Mastodon 导出的 `outbox.json` 转换为可导入 WordPress 的 JSON 格式，并提供完整迁移流程（媒体、主题、导入方案）。

---

## ✨ 项目简介

Mastodon 官方不支持将历史嘟文迁移到新平台。
本项目提供一个**完整的归档解决方案**：

* 📄 转换嘟文 JSON → WordPress 导入格式
* 🖼️ 保留图片 / 视频媒体
* 🏷️ 保留标签（Hashtag）
* 💬 保留回复关系（引用原帖）
* 🧱 生成 Gutenberg（区块编辑器）兼容内容
* 📚 提供完整迁移教程（从导出 → 部署 → 导入）

---

## 🧩 项目结构

```
.
├── script/
│   └── mastodon2wordpress.py  # JSON 转换脚本
├── dist/
│   └── mastodon2wordpress.exe # 可执行文件exe
├── docs/
│   └── guide.md               # 迁移教程（待完善）
├── theme/
│   └── mastodon.zip           # 自定义 WordPress 主题
├── images/                    # 文档配图
└── README.md
```

---

## 🚀 快速开始（脚本使用）

### 1️⃣ 准备 Mastodon 数据

从 Mastodon 导出你的数据（设置 → 导出）：

```
outbox.json
```

---

### 2️⃣ 运行脚本

```bash
python convert.py outbox.json https://your-site.com 1
```

参数说明：

| 参数                    | 说明              |
| --------------------- | --------------- |
| outbox.json           | Mastodon 导出文件   |
| https://your-site.com | 你的 WordPress 域名 |
| 1              | 起始文章编号          |

---

### 3️⃣ 输出结果

生成：

```
output.json
```

可直接用于 WordPress 导入插件**Post Export Import with Media**。

---

### 直接使用 exe（无需 Python）

1. 下载 `dist/mastodon2wordpress.exe`
2. 准备准备 Mastodon 数据 `outbox.json`
3. 拖拽 JSON 到 exe 上运行

---
## 📚 完整迁移教程

👉 👉 👉 **请查看：**

```
docs/guide.md（待完善）
```

包含：

* Mastodon 数据导出
* WordPress 设置与主题安装
* JSON 导入插件使用

---

## 🎨 WordPress 主题

项目中包含一个已配置好的主题：

```
theme/mastodon.zip
```

特点：

* 基于官方主题修改
* 适配 Mastodon 风格阅读
* 支持图片 / 视频展示
* 简洁归档风格

---

## ⚠️ 注意事项

* Mastodon 媒体需要**手动上传到 WordPress**
* JSON 导入依赖第三方插件**Post Export Import with Media**
* 视频默认使用 `<video>` 标签嵌入
* 若导入重复，取决于插件对 `post_title` 的判断

---

## 📌 已实现功能

* [x] 标签提取（Hashtag）
* [x] 媒体提取（图片 / 视频）
* [x] WordPress Block 格式生成
* [x] 自动生成摘要（excerpt）
* [x] 插入文章特色图片
* [x] 标签增强（有媒体 / 有折叠）

---

## 📄 License

MIT License

---

## 🙋‍♂️ 关于

这个项目最初是为了将旧 Mastodon 账号内容迁移到 WordPress 作为长期存档。

如果你也有类似需求，希望这个工具对你有帮助。
