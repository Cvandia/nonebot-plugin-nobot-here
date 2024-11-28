"""
Description: data manager
"""

import json

from dataclasses import dataclass, field
from pathlib import Path
from nonebot import get_driver
from nonebot.log import logger
from nonebot_plugin_alconna import UniMessage
from nonebot_plugin_apscheduler import scheduler

from .config import plugin_config

DRIVER = get_driver()
DATA_FILE = Path(plugin_config.nobot_data_path)


@dataclass
class FixedLengthQueue:
    """固定长度队列"""

    max_length: int
    queue: list[UniMessage] = field(default_factory=list)

    def append(self, item: UniMessage):
        """添加元素到队列末尾，如果超出长度限制，移除最早的元素"""
        self.queue.append(item)
        if len(self.queue) > self.max_length:
            self.queue.pop(0)

    def count(self, item: UniMessage) -> int:
        """统计某个元素在队列中的数量"""
        return self.queue.count(item)

    def remove_all(self, item: UniMessage):
        """移除队列中所有指定元素"""
        self.queue = [i for i in self.queue if i != item]


g_group_data: dict[str, FixedLengthQueue] = {}


def load_data() -> None:
    """加载消息池数据"""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data: dict = json.load(f)
        # 将JSON数据转换为 FixedLengthQueue 实例
        for group_id, message_json in data.items():
            queue_data = [UniMessage.load(message) for message in message_json]
            g_group_data[group_id] = FixedLengthQueue(30, queue_data)
        logger.info("加载消息池数据成功")
    except FileNotFoundError:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write("{}")
            logger.info("消息池数据文件不存在，已创建")
            load_data()
    except Exception as e:
        logger.error(f"加载消息池数据失败: {e}")


def save_data() -> None:
    """保存消息池数据"""
    try:
        data = {
            group_id: [message.dump() for message in queue.queue]
            for group_id, queue in g_group_data.items()
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info("保存消息池数据成功")
    except Exception as e:
        logger.error(f"保存消息池数据失败: {e}")


@DRIVER.on_bot_connect
async def _():
    load_data()

    @scheduler.scheduled_job("interval", minutes=2, id="clear_data")
    async def _():
        g_group_data.clear()


@DRIVER.on_bot_disconnect
async def _():
    save_data()
