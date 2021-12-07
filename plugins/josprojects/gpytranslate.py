#!/usr/bin/env python3
# Copyright (C) @ZauteKm
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
from gpytranslate import Translator
from functools import wraps
from pyrogram import Client
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

tr = Translator()


translated_button = InlineKeyboardMarkup(
     [[
     InlineKeyboardButton(text=f'translated from {language} to {tolanguage}', url='https://cloud.google.com/translate/docs/languages')
     ]]
 )


class google_api_error(Exception):
    pass

def logging_errors(f):
    @wraps(f)
    async def err_log(client: Client, message: Message, *args, **kwargs):
        try:
            return await f(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            await message.chat.leave()
            return
        except Exception as e:
            try:
                await message.reply(
                    text=f'**Error:**\n\n`{type(e).__name__}`: {e}\n\n **forward this message to https://t.me/JOSPSupport if you see this error again, try to forward your message too for better help**'),
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('close this messages', callback_data='close_data')]]
                    disable_web_page_preview=True,
                )
            except ChatWriteForbidden:
                await message.chat.leave()
                return

    return err_log


@Client.on_message(filters.command("poll") & filters.reply)
@logging_errors
async def gen_poll_tr_group_chat(bot, message: Message):
    try:
        if message.reply_to_message.poll:
            replymsg = message.reply_to_message
            poll_options = "\n".join(i["text"] for i in replymsg.poll.options)
            txt_to_tr = f"{replymsg.poll.question}\n{poll_options}"
            if len(message.text.split()) > 1:
                tolanguage = message.command[1]
            else:
                tolanguage = "en"
            translation = await tr(txt_to_tr, targetlang=[tolanguage, "utf-16"])
            translation_text = translation.text
            poll_que = translation_text.split("\n", 1)[0]
            poll_opt = translation_text.splitlines()[1:]
            return await bot.send_poll(
                chat_id=message.chat.id,
                question=poll_que,
                options=poll_opt,
                is_anonymous=replymsg.poll.is_anonymous,
                allows_multiple_answers=replymsg.poll.allows_multiple_answers,
            )
        else:
            return
    except json.decoder.JSONDecodeError:
        raise google_api_error(text='this is not text or this is google translate api limit, please try again later.')


@Client.on_message(
    filters.command(["tr", "tl", "translate"]) & filters.reply
)
@logging_errors
async def translategroup(bot, message: Message) -> None:
    try:
        if message.reply_to_message.poll is None:
            if message.reply_to_message.caption:
                to_translate = message.reply_to_message.caption
            elif message.reply_to_message.text:
                to_translate = message.reply_to_message.text
            else:
                return
            try:
                args = message.text.split()[1].lower()
                if "//" in args:
                    language = args.split("//")[0]
                    tolanguage = args.split("//")[1]
                else:
                    language = await tr.detect(to_translate)
                    tolanguage = args
            except IndexError:
                language = await tr.detect(to_translate)
                tolanguage = "en"
            translation = await tr(
                to_translate, sourcelang=language, targetlang=tolanguage
            )
            await message.reply(
                text=f"`{translation.text}`,
                reply_markup=translated_button
            )
        elif message.reply_to_message.poll is not None:
            options = "\n".join(
                x["text"] for x in message.reply_to_message.poll.options
            )
            to_translate = f"{message.reply_to_message.poll.question}\n\n\n{options}"
            language = await tr.detect(to_translate)
            if len(message.text.split()) > 1:
                tolanguage = message.command[1]
            else:
                tolanguage = "en"
            translation = await tr(
                to_translate, sourcelang=language, targetlang=tolanguage
            )
            await message.reply(
                text=f"`{translation.text}`,
                reply_markup=translated_button
            )
    except json.decoder.JSONDecodeError:
        raise google_api_error(text='this is not text or this is google translate api limit, please try again later.')


@Client.on_message(filters.command("tr") & ~filters.reply)
@logging_errors
async def translategrouptwo(bot, message: Message):
    try:
        if len(message.text.split()) > 1:
            tolanguage = message.command[1]
        else:
            return await message.reply_text(constants.err_must_specify_lang)
        if len(message.text.split()) > 2:
            to_translate = message.text.split(None, 2)[2]
        else:
            return await message.reply_text(constants.err_must_specify_text)
        language = await tr.detect(message.text.split(None, 2)[2])
        translation = await tr(to_translate, sourcelang=language, targetlang=tolanguage)
        await message.reply_text(
            text=f"`{translation.text}`,
            reply_markup=translated_button
        )
    except json.decoder.JSONDecodeError:
        raise google_api_error(text='this is not text or this is google translate api limit, please try again later.')
