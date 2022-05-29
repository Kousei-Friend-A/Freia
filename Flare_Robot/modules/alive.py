import os
import re
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from Flare_Robot.events import register
from Flare_Robot import telethn as tbot


PHOTO = "https://telegra.ph/file/294b0002b4ad05ebf0f38.jpg"


@register(pattern=("/alive"))
async def awake(event):
    TEXT = "**♡ I,m sᴇxʏ ғʟᴀʀᴇ 愛** \n\n"
    TEXT += f"**♡ I'm Working With sᴇxʏ Speed** \n\n"
    TEXT += f"**♡ ғʀᴇɪᴀ: LATEST Version** \n\n"
    TEXT += f"**♡ My Creator: [ ᴀsᴛᴀ](http://t.me/Asta_silva002)** \n\n"
    TEXT += f"**♡ ᴀɴʏ ɪssᴜᴇs ᴄᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ @KamadoSupport** \n\n"
    TEXT += "**♡ ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ 💘💘💘**"
    BUTTON = [
        [
            Button.url("📢 Updates", "https://t.me/Freia_Updates"),
            Button.url("🚑 Support", "https://t.me/KamadoSupport"),
        ]
    ]
    await tbot.send_file(event.chat_id, PHOTO, caption=TEXT, buttons=BUTTON)
