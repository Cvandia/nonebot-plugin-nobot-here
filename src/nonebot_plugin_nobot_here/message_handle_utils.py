"""
Description:
    Utils for handling messages
"""

import json
import random
import asyncio

from nonebot_plugin_alconna import UniMessage
from nonebot.adapters import Bot, Event
from nonebot.log import logger
from pathlib import Path

from .data_manager import FixedLengthQueue

# 随机回复数据文件路径: 该文件下的./random_reply.json
RANDOM_REPLY_DATA_FILE = Path(__file__).parent / "random_reply.json"


async def check_and_send_plusone(
    message_list: FixedLengthQueue, message: UniMessage, bot, event
):
    _cnt = message_list.count(message)
    if _cnt >= 3:
        await message.send(event, bot)
        message_list.remove_all(message)


class RandomReply:
    """随机回复类"""

    def __init__(self):
        """实例化时从文件中加载数据"""
        try:
            with open(RANDOM_REPLY_DATA_FILE, "r", encoding="utf-8") as f:
                data: dict[str, list[str]] = json.load(f)
            self.reply_list: dict[str, list[UniMessage]] = {
                key: [UniMessage.load(message) for message in value]
                for key, value in data.items()
            }
            logger.debug("加载随机回复数据成功")
        except Exception as e:
            logger.error(f"加载随机回复数据失败: {e}")
            self.reply_list = {}

    async def send(self, event: Event, bot: Bot):
        """发送随机回复"""
        # 从dict中随机选择一个key
        if not self.reply_list:
            return
        _random_choice = random.choice(list(self.reply_list.keys()))
        for message in self.reply_list[_random_choice]:
            await message.send(event, bot)
            await asyncio.sleep(random.uniform(0.5, 1.5))
