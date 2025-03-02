from Stella import StellaCli

from Stella.helper import custom_filter
from Stella.helper.time_checker import time_string_helper

from Stella.database.antiflood_mongo import (
    get_flood,
    get_floodlimit,
    get_antiflood_mode
)

@StellaCli.on_message(custom_filter.command(commands=('flood')))
async def flood(client, message):

    chat_id = message.chat.id
    if not get_flood(chat_id):
        await message.reply(
            "This chat is not currently enforcing flood control."
        )
        return 
    
    FLOOD_LIMIT = get_floodlimit(chat_id)
    FLOOD_MODE, FLOOD_TIME = get_antiflood_mode(chat_id)
    text = (
        f"This chat is currently enforcing flood control after {FLOOD_LIMIT} messages. "
    )
    if FLOOD_MODE == 1:
        text += "Any users sending more than that amount of messages will be banned."
    elif FLOOD_MODE == 2:
        text += "Any users sending more than that amount of messages will be muted."
    elif FLOOD_MODE == 3:
        text += "Any users sending more than that amount of messages will be kicked."
    elif FLOOD_MODE == 4:
        time_limit, time_format = time_string_helper(FLOOD_TIME)
        text += f"Any users sending more than that amount of messages will be temporarily banned for {time_limit} {time_format}."
    elif FLOOD_MODE == 5:
        time_limit, time_format = time_string_helper(FLOOD_TIME)
        text += f"Any users sending more than that amount of messages will be temporarily muted for {time_limit} {time_format}."

    await message.reply(
        text
    )