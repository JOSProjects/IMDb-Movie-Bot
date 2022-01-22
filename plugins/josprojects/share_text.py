import os
from pyrogram import Client, filters
from urllib.parse import quote
from info import SUPPORT_CHAT

def share_link(text: str) -> str:
    return "**Here is Your Sharing Text 👇**\n\nhttps://t.me/share/url?url=" + quote(text)

@Client.on_message(filters.command(["share", "sharetext", "st", "stxt", "shtxt", "shtext"]))
async def groupmsg(client, message):
    k = await message.reply_text("**Making...**")
    reply = message.reply_to_message
    if not reply:
        await k.edit("`Reply any Message`")
        return
    input_split = message.text.split(None, 1)
    if len(input_split) == 2:
        input_text = input_split[1]
    elif reply and (reply.text or reply.caption):
        input_text = reply.text or reply.caption
    else:
        await k.edit(
            f"""Something wrong Ask @{SUPPORT_CHAT}""",
        )
        return
    await k.edit(share_link(input_text))
        
