"""
Description:
    Config file for nonebot_plugin_nobot_here
"""

from pydantic import BaseModel
from nonebot.plugin import get_plugin_config


class Config(BaseModel):
    handle_group: bool = True
    nobot_data_path: str = "./data/no_bot/data.json"
    random_reply_data_path: str = "./data/no_bot/random_reply.json"


plugin_config = get_plugin_config(Config)
