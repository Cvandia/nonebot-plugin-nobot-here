"""
Description:
    __init__ file for package installation
"""

from contextlib import suppress
from nonebot import require
from .config import Config

require("nonebot_plugin-alconna") 

from . import matcher as _macher # noqa


with suppress(Exception):
    from nonebot.plugin import PluginMetadata, inherit_supported_adapters

    __plugin_meta__ = PluginMetadata(
        name="No bot here!",
        description="群里有机器人？哪里有机器人，咱不是！",
        usage=None,
        homepage="https://github.com/Cvandia/nonebot-plugin-nobot-here",
        config=Config,
        type="application",
        supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
        extra={"author": "Cvandia", "email": "1141538825@qq.com"},
    )
