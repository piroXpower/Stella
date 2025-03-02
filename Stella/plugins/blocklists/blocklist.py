import html

from Stella import StellaCli

from Stella.helper import custom_filter
from Stella.helper.chat_status import isUserAdmin

from Stella.database.blocklists_mongo import get_blocklist

@StellaCli.on_message(custom_filter.command(commands=['blocklist', 'blacklist']))
async def blocklist(client, message):

    chat_id = message.chat.id 
    chat_title = message.chat.title
    if not await isUserAdmin(message):
        return
    
    BLOCKLIST_DATA = get_blocklist(chat_id)
    if (
        BLOCKLIST_DATA is None
        or len(BLOCKLIST_DATA) == 0
    ):
        await message.reply(
            f"No blocklist filters active in {html.escape(chat_title)}!"
        )
        return

    BLOCKLIST_ITMES = []
    for blocklist_array in BLOCKLIST_DATA:
        BLOCKLIST_ITMES.append(blocklist_array['blocklist_text'])
    
    blocklist_header = f"The following blocklist filters are currently active in {html.escape(chat_title)}:\n"
    for block_itmes in BLOCKLIST_ITMES:
        blocklist_name = f"- `{block_itmes}`\n"
        blocklist_header += blocklist_name

    await message.reply(
        blocklist_header,
        quote=True
    )