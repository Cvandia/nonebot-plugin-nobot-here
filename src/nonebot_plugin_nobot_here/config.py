"""
Description:
    Config file for nonebot_plugin_nobot_here
"""

from nonebot.plugin import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    handle_group: bool = True
    nobot_data_path: str = "./data/no_bot/data.json"


plugin_config = get_plugin_config(Config)
