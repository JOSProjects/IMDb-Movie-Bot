import os
import aiohttp
import json
from pyrogram import Client, filters, emoji
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


m = None
i = 0
a = None
query = None


@Client.on_message(filters.command(["torrent", "tor"]))
async def torrent(_, message):
    global m
    global i
    global a
    global query
    try:
        await message.delete()
    except:
        pass
    if len(message.command) < 2:
        await message.reply_text("`/torrent <Movie Name>`")
        return
    query = message.text.split(None, 1)[1].replace(" ", "%20")
    m = await message.reply_text("Searching\nThis might take a while")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://itor.api-zero.workers.dev/?name={query}") \
                    as resp:
                a = json.loads(await resp.text())
    except:
        await m.edit("Found Nothing.")
        return
    result = (
        f"**Page - {i+1}**\n\n"
        f"**🎬 Name :** {a[i]['name']}\n"
        f"**🧲 Link :** `{a[i]['link']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"{emoji.CROSS_MARK} Close",
                                         callback_data="close_data"),
                    InlineKeyboardButton(f"Next ⏩",
                                         callback_data="next_tor")
                ]
            ]
        ),
        parse_mode="markdown",
    )


@Client.on_callback_query(filters.regex("next_tor"))
async def callback_query_next(_, message):
    global i
    global m
    global a
    global query
    i += 1
    result = (
        f"**Page - {i+1}**\n\n"
        f"**🎬 Name :** {a[i]['name']}\n"
        f"**🧲 Link :** `{a[i]['link']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"⏪ Back",
                                         callback_data="back_tor"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="close_data"),
                    InlineKeyboardButton(f"Next ⏩",
                                         callback_data="next_tor")
                    
                ]
            ]
        ),
        parse_mode="markdown",
    )


@Client.on_callback_query(filters.regex("back_tor"))
async def callback_query_previous(_, message):
    global i
    global m
    global a
    global query
    i -= 1
    result = (
        f"**Page - {i+1}**\n\n"
        f"**🎬 Name:** {a[i]['name']}\n"
        f"**🧲 Link:** `{a[i]['link']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"⏪ Back",
                                         callback_data="back_tor"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="close_data"),
                    InlineKeyboardButton(f"Next ⏩",
                                         callback_data="next_tor")
                ]
            ]
        ),
        parse_mode="markdown",
    )
