"""
吃什么 - AstrBot QQ 群聊插件

当群成员发送含触发关键词（默认"吃什么"）的消息时，
机器人随机回复一种食物名称并附带对应图片。

数据来源：data/foods.json（菜品列表）+ images/ 目录（食物图片）
纯本地存储，无外部 API 依赖。
"""

import os
import json
import random

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star
import astrbot.api.message_components as Comp
from astrbot.api import logger, AstrBotConfig


class WhatToEat(Star):
    """
    "吃什么" 插件主类。

    继承 Star（AstrBot 插件基类），通过 @filter.regex()
    被动监听群消息（无需唤醒前缀），匹配关键词后随机推荐食物。
    """

    def __init__(self, context: Context, config: AstrBotConfig):
        """
        插件初始化：加载菜品数据和配置。

        context 由 AstrBot 框架注入，提供插件运行所需的上下文信息。
        config 由 AstrBot 框架自动传入，对应 _conf_schema.json 定义的配置项。
        """
        super().__init__(context)

        self.config = config

        # 插件根目录的绝对路径，用于拼接数据文件和图片文件的路径
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))

        # 加载 foods.json
        self.foods = self._load_foods()

        # 顺序推荐模式的游标（仅在 enable_random=false 时使用）
        self._seq_index = 0

        logger.info(f"吃什么 插件已加载，共 {len(self.foods)} 道菜品")

    # ──────────────────────────────────────────────
    # 数据加载
    # ──────────────────────────────────────────────

    def _load_foods(self) -> list[dict]:
        """
        从 data/foods.json 加载菜品列表。

        返回 list[dict]，每个 dict 包含：
          - name: 菜品中文名称
          - image: 图片相对于插件根目录的路径

        文件不存在或格式错误时返回空列表，不会抛出异常。
        """
        foods_path = os.path.join(self.plugin_dir, "data", "foods.json")

        if not os.path.exists(foods_path):
            logger.error(f"菜品数据文件不存在: {foods_path}")
            return []

        try:
            with open(foods_path, "r", encoding="utf-8") as f:
                foods = json.load(f)

            # 基础校验：必须是列表
            if not isinstance(foods, list):
                logger.error("foods.json 格式错误：根元素应为数组")
                return []

            # 过滤掉缺少 name 字段的无效条目
            valid = [item for item in foods if isinstance(item, dict) and "name" in item]
            if len(valid) != len(foods):
                logger.warning(f"foods.json 中有 {len(foods) - len(valid)} 条无效数据已被跳过")

            return valid

        except json.JSONDecodeError as e:
            logger.error(f"foods.json 解析失败: {e}")
            return []
        except Exception as e:
            logger.error(f"加载 foods.json 时发生未知错误: {e}")
            return []

    # ──────────────────────────────────────────────
    # 消息处理
    # ──────────────────────────────────────────────

    @filter.regex(r"吃什么")
    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    @filter.platform_adapter_type(filter.PlatformAdapterType.AIOCQHTTP)
    async def on_what_to_eat(self, event: AstrMessageEvent):
        """
        监听 QQ 群消息，匹配触发关键词后回复食物推荐。

        装饰器说明：
          - @filter.regex: 用正则匹配消息正文，无需唤醒前缀（用户无需 / 或 @机器人）
          - @filter.event_message_type: 限制仅群聊消息
          - @filter.platform_adapter_type: 限制仅 QQ 平台

        三个条件同时满足（AND 逻辑），消息才会进入此 handler。
        """
        # ── 1. 检查菜品数据是否可用 ──
        if not self.foods:
            yield event.plain_result("菜单还没准备好，请联系管理员检查插件数据~")
            return

        # ── 2. 选取一道菜 ──
        food = self._pick_food()

        # ── 3. 构建回复消息链（文本 + 图片） ──
        chain = self._build_reply(food)

        # ── 4. 发送 ──
        yield event.chain_result(chain)

    # ──────────────────────────────────────────────
    # 辅助方法
    # ──────────────────────────────────────────────

    def _pick_food(self) -> dict:
        """
        根据配置选取一道菜。

        enable_random=true  → 纯随机
        enable_random=false → 按列表顺序循环
        """
        enable_random = self.config.get("enable_random", True)

        if enable_random:
            return random.choice(self.foods)
        else:
            # 顺序循环：取当前索引，然后 +1（超出则回到开头）
            food = self.foods[self._seq_index]
            self._seq_index = (self._seq_index + 1) % len(self.foods)
            return food

    def _build_reply(self, food: dict) -> list:
        """
        构建回复消息链：一段文字 + 一张图片。

        参数 food: {"name": "红烧肉", "image": "images/hongshaorou.jpg"}

        返回 list[Comp]，可直接传给 event.chain_result()。

        如果图片文件不存在，只返回文字不会崩溃。
        """
        chain = [
            Comp.Plain(f"今天建议吃：{food['name']} 😋"),
        ]

        # 尝试附加图片
        image_rel_path = food.get("image", "")
        if image_rel_path:
            # 拼接为绝对路径
            image_abs_path = os.path.join(self.plugin_dir, image_rel_path)

            if os.path.exists(image_abs_path):
                chain.append(Comp.Image.fromFileSystem(image_abs_path))
            else:
                logger.warning(f"图片文件不存在: {image_abs_path}（菜品: {food['name']}）")

        return chain

    # ──────────────────────────────────────────────
    # 生命周期
    # ──────────────────────────────────────────────

    async def terminate(self):
        """
        插件被卸载/禁用时调用。

        这里无需特殊清理（无网络连接、无后台任务），
        保留空实现以便将来扩展。
        """
        logger.info("吃什么 插件已卸载")
