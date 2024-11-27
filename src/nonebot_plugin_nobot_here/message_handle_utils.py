"""
Description:
    Utils for handling messages
"""

from nonebot_plugin_alconna import UniMessage
from .data_manager import data_manager


async def check_and_send_plusone(group_id: str, group_data: list, bot, event) -> None:
    """
    Check if the bot should send a plusone message
    - if true, send the plusone message and delete the last 3 messages
    - if false, do nothing

    Args:
        group_id (str): The group id
        group_data (list): The group data
        bot (Bot): The bot
        event (Event): The event

    Returns:
        None
    """
    if len(group_data) >= 3 and group_data[-1] == group_data[-2] == group_data[-3]:
        await UniMessage.load(group_data[-1]).send(event, bot)
        del group_data[-3:]
        data_manager.set_data(group_id, group_data)
