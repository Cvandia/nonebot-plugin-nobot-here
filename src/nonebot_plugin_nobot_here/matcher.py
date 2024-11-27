"""
Description:
    Matcher and main logic for the plugin
"""

import random
from nonebot import get_driver
from nonebot.adapters import Event, Bot
from nonebot.message import event_preprocessor
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot_plugin_alconna import UniMessage, on_alconna, Alconna, MultiVar, Args
from nonebot_plugin_apscheduler import scheduler

from .data_manager import data_manager
from .message_handle_utils import check_and_send_plusone

DRIVER = get_driver()

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

    # revert message to json
    _unimessage = await UniMessage.generate(message=raw_message, bot=bot)
    _message_json = _unimessage.dump()

    # get group data and append json message to it
    group_data = data_manager.get_data(group_id) or []
    group_data.append(_message_json)
    data_manager.set_data(group_id, group_data)

    # Bot Repeat
    await check_and_send_plusone(group_id, group_data, bot, event)

    # TODO: Bot Random send message to act like a human
    if len(group_data) >= 5:
        if random.random() < 0.1:
            await UniMessage.text("我不是机器人！").send(event, bot)  # test message
            data_manager.del_data(group_id)


@DRIVER.on_bot_connect
async def startup():
    if not data_manager.data_path.exists():
        data_manager.save_data()
    data_manager.load_data()

    # clear group message count every minute
    @scheduler.scheduled_job("interval", minutes=1, id="clear_group_message_count")
    async def _():
        data_manager.clear_data()


@DRIVER.on_bot_disconnect
async def shutdown():
    scheduler.shutdown()
    data_manager.save_data()
