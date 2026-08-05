# 🍽️ 吃什么

> 专治"今天吃什么"选择困难症——群友发一句含"吃什么"的消息，机器人随机推荐一道菜，图文并茂。

[![AstrBot](https://img.shields.io/badge/AstrBot-%3E%3D4.16-blue)](https://github.com/AstrBotDevs/AstrBot)
[![Platform](https://img.shields.io/badge/platform-QQ_(aiocqhttp)-green)](#)
[![Version](https://img.shields.io/badge/version-1.0.0-orange)](metadata.yaml)
[![License](https://img.shields.io/badge/license-MIT-9cf)](LICENSE)
[![Author](https://img.shields.io/badge/author-wjn1121-lightgrey)](https://github.com/wjn1121)

---

## ✨ 功能特性

- 🎲 **随机推荐**：每次随机从菜品库中抽取一道，告别选择困难
- 🖼️ **图文并茂**：每道菜配有实拍图片，回复直观有食欲
- 🔌 **被动匹配**：自然语言触发，消息中包含"吃什么"即可，无需 `/` 前缀或 @机器人
- 📦 **纯本地运行**：数据+图片全在本地，零网络依赖，响应即时
- 🛡️ **降级容错**：图片缺失时只返回文字，不会崩溃
- ⚙️ **可视化配置**：WebUI 面板直接调节，无需编辑配置文件

---

## 🎬 效果演示

```
群友: 中午不知道吃什么，好纠结啊
Bot:   🍽️ 今天吃：红烧肉！
      [红烧肉图片]
```

```
群友: 晚上吃什么
Bot:   🍽️ 今天吃：螺蛳粉！
      [螺蛳粉图片]
```

---

## 📥 安装方式

### 方式一：插件市场（推荐）

在 AstrBot WebUI → 插件市场 → 搜索「**吃什么**」→ 一键安装

### 方式二：手动安装

```bash
# 克隆到 AstrBot 插件目录
cd AstrBot/data/plugins/
git clone https://github.com/wjn1121/astrbot_plugin_chishenme.git
```

安装后重启插件即可生效，无需额外配置。

---

## 🎯 触发规则

| 你说的话 | 是否触发 |
|----------|:------:|
| `吃什么` | ✅ |
| `今天吃什么` | ✅ |
| `中午吃什么啊好饿` | ✅ |
| `不知道晚上吃什么` | ✅ |
| `吃了吗` | ❌ |
| `这家店好好吃` | ❌ |
| `吃货` | ❌ |

> 💡 仅匹配包含连续三个字「**吃什么**」的消息，从「吃饭」「好吃」等词不会被误触发。

**生效范围**：仅 **QQ 群聊**（aiocqhttp 适配器），私聊及其他平台不触发。

---

## ⚙️ 配置项

在 AstrBot WebUI → 插件配置面板中可调：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enable_random` | 布尔 | `true` | `true` = 每次随机推荐；`false` = 按列表顺序循环 |

---

## 🍜 内置菜品

插件内置 **80+ 道菜品**，涵盖八大菜系、地方小吃、异国料理，每道配有图片。

<details>
<summary>📋 点击展开完整菜单</summary>

红烧肉 · 宫保鸡丁 · 麻婆豆腐 · 糖醋里脊 · 鱼香肉丝 · 回锅肉 · 水煮鱼 · 酸菜鱼 · 辣子鸡 · 东坡肉 · 北京烤鸭 · 小笼包 · 火锅 · 麻辣烫 · 兰州拉面 · 炸酱面 · 蛋炒饭 · 扬州炒饭 · 饺子 · 馄饨 · 烤串 · 黄焖鸡 · 番茄炒蛋 · 地三鲜 · 干锅花菜 · 酸辣土豆丝 · 蒜蓉西兰花 · 可乐鸡翅 · 糖醋排骨 · 毛血旺 · KFC · 螺蛳粉 · 煲仔饭 · 叉烧 · 肠粉 · 煎饼果子 · 肉夹馍 · 凉皮 · 烤鱼 · 麻辣香锅 · 炒河粉 · 锅包肉 · 水煮肉片 · 粉蒸肉 · 牛肉面 · 葱油拌面 · 麻辣拌 · 烤羊排 · 鸡公煲 · 盖浇饭 · 炒面 · 生煎 · 烧卖 · 春卷 · 煎饺 · 灌汤包 · 卤肉饭 · 酸素可乐 · 秘制冷却水 · 鱼雷天妇罗 · 海军咖喱 · 皇家料理 · 满汉全席 · 脆皮烧鸽 · 今州冒菜 · 龙抬头 · 油辣豆腐 · 森栖锅 · 酿肉豆腐 · 果木烟熏鸽 · 冠军冒菜 · 绿野锅 · 怪味铛铛蟹 · 怪味当当蟹 · 荣耀烤肉套餐 · 重州麻辣豆腐 · 青云鲞 · 星声 · 月相 · 吃白饭

</details>

---

## ➕ 自定义菜品

1. 将新图片放入 `images/` 目录（支持 jpg / png）
2. 在 `data/foods.json` 中追加一条：

```json
{
  "name": "你的菜品名",
  "image": "images/your-food.jpg"
}
```

3. 重载插件即可生效，无需重启 AstrBot。

---

## 📁 目录结构

```
astrbot_plugin_chishenme/
├── main.py               # 插件入口，核心逻辑
├── metadata.yaml         # 插件元信息（市场显示用）
├── _conf_schema.json     # WebUI 可视化配置定义
├── README.md             # 本文件
├── data/
│   └── foods.json        # 菜品列表（JSON 数组格式）
└── images/               # 食物图片（80+ 张）
```

---

## 🆕 更新日志

### v1.0.1

- ✨ 菜品数量从 30 道扩充至 80+ 道
- 📝 完善 README 文档

### v1.0.0

- 🎉 初始发布
- 🍜 内置 30 道经典中餐
- ⚙️ 支持 WebUI 配置随机/顺序模式

---

## 🔧 技术栈

- **零外部依赖**：仅使用 AstrBot SDK 内置模块，无需 `pip install`
- **纯本地存储**：JSON + 本地图片，无外部 API 调用
- **自然语言匹配**：`@filter.regex(r"吃什么")` 被动监听
- **事件过滤**：通过装饰器叠加限定群聊 + QQ 平台

---

## 🔗 参考资源

| 资源 | 链接 |
|------|------|
| AstrBot 插件开发指南 | https://docs.astrbot.app/dev/star/plugin-new.html |
| 消息事件监听 | https://docs.astrbot.app/dev/star/guides/listen-message-event.html |
| 类似插件 astrbot_plugin_cook | https://github.com/Niloux/astrbot_plugin_cook |
| AstrBot 主仓库 | https://github.com/AstrBotDevs/AstrBot |

---

## 🙋 FAQ

**Q: 为什么不用 `/吃什么` 指令？**
A: 群聊是自然语言场景，"中午吃什么啊"比 `/吃什么` 更符合聊天直觉，降低使用门槛。

**Q: 能触发"吃啥"吗？**
A: 目前固定匹配"吃什么"。如需修改，编辑 `main.py` 中的正则表达式后重载插件即可。

**Q: 图片不显示？**
A: 检查 `images/` 目录下是否有对应文件，以及 `data/foods.json` 中的 `image` 路径是否正确。图片缺失时插件会自动降级为纯文字回复。

**Q: 可以接入 AI 生成推荐吗？**
A: 当前版本为纯本地随机推荐。如需 AI 功能，欢迎提交 PR 或在 QQ 群反馈。

---

## 📞 联系作者

- **QQ 群**：1038882918
- **GitHub**：[@wjn1121](https://github.com/wjn1121)

---

<p align="center">如果这个插件帮你解决了"今天吃什么"的烦恼，请点个 ⭐ Star 支持一下～</p>
