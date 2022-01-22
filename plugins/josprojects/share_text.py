import os
from pyrogram import Client, filters
from urllib.parse import quote
from info import SUPPORT_CHAT

def share_link(text: str) -> str:
    return "**Here is Your Sharing Text 👇**\n\nhttps://t.me/share/url?url=" + quote(text)

@Client.on_message(filters.command(["share", "sharetext", "st", "stxt", "shtxt", "shtext"]))
async def groupmsg(client, message):
    reply = message.reply_to_message
    input_split = message.text.split(None, 1)
    if len(input_split) == 2:
        input_text = input_split[1]
    elif reply and (reply.text or reply.caption):
        input_text = reply.text or reply.caption
    else:
        await message.reply_text(
            text=f"Something went wrong 😑😑,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Support Chat", url=f"https://t.me/{SUPPORT_CHAT}")
                    ]                
                ]
            ),
            reply_to_message_id=message.message_id
        )
        )
        return
    await message.reply_text(share_link(input_text))

        
