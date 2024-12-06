"""
Description:
    Matcher and main logic for the plugin
"""

import secrets

from nonebot.adapters import Bot, Event
from nonebot.log import logger
from nonebot.message import event_preprocessor
from nonebot.rule import to_me
from nonebot_plugin_alconna import Alconna, Args, MultiVar, UniMessage, on_alconna

from .data_manager import FixedLengthQueue, g_group_data
from .message_handle_utils import RandomReply, check_and_send_plusone

add_text = on_alconna(
    Alconna(
        ["添加词条", "添加句子"],
        Args["texts", MultiVar(str, "*")],
    ),
    rule=to_me(),
)

view_text = on_alconna("查看全部词条", aliases={"查看全部句子"}, rule=to_me())

del_text = on_alconna(
    Alconna(
        ["删除词条", "删除句子"],
        Args["indexs", MultiVar(int, "*")],
    ),
    rule=to_me(),
)


@event_preprocessor
async def handle_message(bot: Bot, event: Event):
    # global g_group_data
    """
    Handle messages before they are processed by the matchers
    """
    if event.get_type() != "message":
        return

    group_id = getattr(event, "group_id", None)
    if not group_id:
        logger.warning("Event does not have 'group_id' attribute")
        return

    group_id = str(group_id)
    raw_message = event.get_message()
    if not raw_message:
        return

    # revert message to UniMessage
    _unimessage = await UniMessage.generate(message=raw_message, bot=bot)

    # store message in the group data
    if group_id not in g_group_data:
        g_group_data[group_id] = FixedLengthQueue(max_length=30)
    g_group_data[group_id].append(item=_unimessage)

    await check_and_send_plusone(g_group_data[group_id], _unimessage, bot, event)
    QUEUE_LEN = 10
    RANDOM_REPLY_PROB = 50
    _totle_len = len(g_group_data[group_id].queue)
    if _totle_len >= QUEUE_LEN and secrets.randbelow(100) < RANDOM_REPLY_PROB:
        random_reply = RandomReply()
        await random_reply.send(event, bot)
        g_group_data[group_id].queue.clear()
