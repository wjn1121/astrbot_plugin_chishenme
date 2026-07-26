# 🍽️ 吃什么 — AstrBot QQ 群聊插件

> 专治"今天吃什么"选择困难症。群友发一句"吃什么"，机器人随机推荐一道菜，图文并茂。

[![AstrBot](https://img.shields.io/badge/AstrBot-%3E%3D4.16-blue)](https://github.com/AstrBotDevs/AstrBot)
[![Platform](https://img.shields.io/badge/platform-QQ_(aiocqhttp)-green)](#)
![Version](https://img.shields.io/badge/version-1.0.0-orange)
[![Author](https://img.shields.io/badge/author-wjn1121-lightgrey)](https://github.com/wjn1121)

---

## ⚡ 快速开始

1. **安装插件**：在 AstrBot WebUI 插件市场中搜索「吃什么」一键安装，或手动放入 `data/plugins/astrbot_plugin_chishenme/`
2. **重启插件**：安装后自动加载，无需额外配置
3. **群里发一句** `吃什么`（或 `今天吃什么`、`中午吃什么` 等任意包含"吃什么"的消息）
4. **机器人回复**：一段文字推荐 + 一张食物图片

就这么简单，不需要任何 API Key、不需要联网、不需要 `/` 指令前缀。

---

## 🎯 触发方式

**被动关键词匹配**——群友在消息中任意位置提到"吃什么"即触发，无需 @机器人，无需斜杠前缀。

| 你说 | 触发？ |
|------|:---:|
| `吃什么` | ✅ |
| `今天吃什么` | ✅ |
| `中午吃什么啊好饿` | ✅ |
| `不知道晚上吃什么` | ✅ |
| `吃饭了吗` | ❌ |
| `这家店好好吃` | ❌ |

> 💡 只匹配包含「吃什么」三个字的群消息，"吃饭""好吃"等不会误触发。

**限制范围**：仅在 **QQ 群聊** 中生效，私聊和其他平台不会触发。

---

## ⚙️ 配置

在 WebUI 插件配置面板中可调：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enable_random` | 布尔 | `true` | `true` 每次随机推荐；`false` 按列表顺序循环推荐 |

---

## 🍜 内置菜品

插件内置 **30 道经典中餐**，每道配有图片：

红烧肉 · 宫保鸡丁 · 麻婆豆腐 · 糖醋里脊 · 鱼香肉丝 · 回锅肉 · 水煮鱼 · 酸菜鱼 · 辣子鸡 · 东坡肉 · 北京烤鸭 · 小笼包 · 火锅 · 麻辣烫 · 兰州拉面 · 炸酱面 · 蛋炒饭 · 扬州炒饭 · 饺子 · 馄饨 · 烤串 · 黄焖鸡 · 番茄炒蛋 · 地三鲜 · 干锅花菜 · 酸辣土豆丝 · 蒜蓉西兰花 · 可乐鸡翅 · 糖醋排骨 · 毛血旺

---

## ➕ 自定义菜品

想加自己的菜？两步搞定：

1. 把图片放进 `images/` 目录（支持 jpg/png）
2. 在 `data/foods.json` 中追加一条：

```json
{
  "name": "螺蛳粉",
  "image": "images/luosifen.jpg"
}
```

重载插件即可生效。无需重启 AstrBot。

---

## 📁 目录结构

```
astrbot_plugin_chishenme/
├── main.py               # 插件入口
├── metadata.yaml         # 插件元信息
├── _conf_schema.json     # WebUI 配置定义
├── README.md             # 本文件
├── data/
│   └── foods.json        # 菜品列表（JSON 格式）
└── images/               # 食物图片（30 张）
    ├── hongshaorou.jpg
    ├── gongbaojiding.jpg
    └── ...
```

---

## 🔧 技术特点

- **零依赖**：无外部 pip 包，仅用 AstrBot SDK 内置模块
- **纯本地**：菜品数据和图片全部存储于插件目录，无网络请求，响应即时
- **降级容错**：图片文件缺失时只返回文字推荐，不会崩溃
- **自然语言**：基于 `@filter.regex` 被动监听，比 `/` 指令更符合聊天场景

---

## 📋 兼容性

| 项目 | 要求 |
|------|------|
| AstrBot | ≥ 4.16，< 5 |
| 平台 | QQ（aiocqhttp 适配器） |
| Python | 随 AstrBot 环境 |

---

## 🙋 FAQ

**Q: 为什么不用 `/吃什么` 指令？**
A: 群里聊天是自然语言，"中午吃什么啊" 比 `/吃什么` 更符合直觉。`@filter.regex` 被动匹配更贴合这个场景。

**Q: 能改成"吃啥"触发吗？**
A: 目前固定匹配"吃什么"三个字。需要修改可编辑 `main.py` 第 98 行的正则表达式后重载插件。

**Q: 图片不显示怎么办？**
A: 检查 `images/` 目录下是否有对应文件，以及 `data/foods.json` 中的 `image` 路径是否正确。

---

## 📞 联系作者

- **QQ 群**：1038882918
- **GitHub**：[@wjn1121](https://github.com/wjn1121)
