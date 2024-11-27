"""
Description:
    Main logic for handling messages
"""

from nonebot.adapters import Event, Bot
from nonebot_plugin_alconna import UniMessage
from nonebot.plugin.on import on_message

from .config import plugin_config as config

matcher = on_message(priority=10, block=True)


@matcher.handle()
async def handle(bot: Bot, event: Event):
    if config.db_url:
        await UniMessage.text("no bot here!").send()
