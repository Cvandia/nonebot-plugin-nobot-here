"""
Description:
    Config file for nonebot_plugin_nobot_here
"""

from pydantic import BaseModel
from nonebot.plugin import get_plugin_config


class Config(BaseModel):
    db_url: str


plugin_config = get_plugin_config(Config)
