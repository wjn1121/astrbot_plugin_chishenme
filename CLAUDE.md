# 吃什么 - AstrBot QQ 群聊插件

## 项目概述

一个 AstrBot 插件，用于 QQ 群聊场景。当群成员发送含关键词"吃什么"的消息时，机器人随机回复一种食物名称并附带对应图片。

- **触发方式**：自然语言关键词匹配（"中午吃什么"、"今天吃什么" 等均可触发）
- **数据存储**：纯本地 JSON + 图片文件，无外部 API 依赖
- **目标平台**：QQ（aiocqhttp 适配器）

## 目录结构

```
astrbot_plugin_chishenme/         # 插件根目录，放入 AstrBot/data/plugins/
├── main.py                       # 插件入口，核心逻辑
├── metadata.yaml                 # 插件元信息（名称、版本、作者等）
├── _conf_schema.json             # WebUI 可视化配置项定义
├── data/
│   └── foods.json                # 菜品列表，每项包含名称和图片相对路径
└── images/                       # 食物图片，文件名与 foods.json 中的路径对应
    ├── hongshaorou.jpg
    ├── gongbaojiding.jpg
    └── ...
```

## 数据格式

### `data/foods.json`

```json
[
  {
    "name": "红烧肉",
    "image": "images/hongshaorou.jpg"
  },
  {
    "name": "宫保鸡丁",
    "image": "images/gongbaojiding.jpg"
  }
]
```

- `name`：展示给用户的中文菜名
- `image`：图片文件相对于插件根目录的路径

### 扩展方式

1. 将新图片放入 `images/` 目录
2. 在 `data/foods.json` 中追加一条记录
3. 重载插件即可生效

## 核心逻辑流程

```
群消息 → @filter.regex(r"吃什么") 监听（无需唤醒前缀）
  → @filter.event_message_type(GROUP_MESSAGE) → 仅群聊
  → @filter.platform_adapter_type(AIOCQHTTP)   → 仅 QQ
  → 三个条件同时满足 → 进入 handler
  → random.choice(foods) 随机选一条
  → os.path.join(plugin_dir, food["image"]) 拼接图片路径
  → chain = [Comp.Plain(...), Comp.Image.fromFileSystem(...)]
  → yield event.chain_result(chain) 回复
```

## 关键设计决策

### 为何不用 @filter.command()

用户输入是自然语言（"中午吃什么"），而非固定命令（`/吃什么`）。使用 `@filter.regex()` 做被动关键词匹配，无需用户 @机器人或输入 `/` 前缀。

### 为何图片存本地而非 URL

- 无网络依赖，响应即时
- 名称和图片保证匹配（URL 可能失效或内容变化）
- 无需注册任何 API、无需填 key

### 图片缺失时的降级

如果 `food["image"]` 指向的文件不存在，只返回文字，不崩溃：

```python
if os.path.exists(image_path):
    chain.append(Comp.Image.fromFileSystem(image_path))
# 否则仅返回文字
```

### 平台限制

通过装饰器叠加限制仅在 QQ 群聊生效，避免私聊或其他平台误触发：

```python
@filter.regex(r"吃什么")
@filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
@filter.platform_adapter_type(filter.PlatformAdapterType.AIOCQHTTP)
```

## AstrBot 插件规范要点

- 主类必须继承 `astrbot.api.star.Star`
- 入口文件必须命名为 `main.py`
- handler 前两个参数固定为 `self` 和 `event: AstrMessageEvent`
- 回复方式推荐 `yield event.chain_result()` 或 `yield event.plain_result()`
- 使用 `event.send()` 可在事件已被其他插件处理后仍强制回复
- 持久化数据写入 `data/` 目录（相对于 AstrBot 数据目录），不要写插件自身目录
- 异步网络请求使用 `aiohttp` 或 `httpx`，不要用同步的 `requests`（本插件不涉及）

## 依赖

- **无外部 pip 依赖**，仅使用 AstrBot SDK 内置模块
- AstrBot >= v4.16

## 参考资源

| 资源 | 链接 |
|------|------|
| AstrBot 插件开发指南 | https://docs.astrbot.app/dev/star/plugin-new.html |
| 消息事件监听 | https://docs.astrbot.app/dev/star/guides/listen-message-event.html |
| 消息发送 | https://docs.astrbot.app/dev/star/guides/send-message.html |
| 类似插件 astrbot_plugin_cook | https://github.com/Niloux/astrbot_plugin_cook |
| AstrBot 主仓库 | https://github.com/AstrBotDevs/AstrBot |
