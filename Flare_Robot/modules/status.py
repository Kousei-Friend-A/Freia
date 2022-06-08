import os
import re
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from Flare_Robot.events import register
from Flare_Robot import telethn as tbot

import html
import requests
import datetime
import platform
import time
import subprocess

from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
from platform import python_version
from telethon import events, Button

from telegram import __version__ as ptbver
from telegram.ext import CallbackContext, CommandHandler
from telegram.error import BadRequest
    

import Flare_Robot.modules.sql.userinfo_sql as sql
from Flare_Robot.events import register
from Flare_Robot import (
    dispatcher,
    StartTime
)
from Flare_Robot.__main__ import STATS, TOKEN, USER_INFO
from Flare_Robot.modules.disable import DisableAbleCommandHandler
from Flare_Robot.modules.helper_funcs.chat_status import sudo_plus


PHOTO= "https://telegra.ph/file/ad6084cb47b9c90fd10d6.jpg"

@sudoplus
@register(pattern=("/status"))
async def awake(event):
    uptime = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    status = "╒═══「 System Statistics 」\n\n"
    status += "➢ System Start time: " + str(uptime) + "\n"
    uname = platform.uname()
    status += "➢ Python Version: " + python_version() + "\n"
    status += "➢ python-Telegram-Bot: " + str(ptbver) + "\n"
    BUTTON = [
        [
            Button.url("📢 Updates", "https://t.me/Freia_Updates"),
            Button.url("🚑 Support", "https://t.me/KamadoSupport"),
        ],
        [
            Button.url("◆|Owner|◆", "https://t.me/Asta_silva002"),
        ]
    ]
    await tbot.send_file(event.chat_id, PHOTO, caption=status + "\nBot statistics:\n" + "\n".join([mod.__stats__() for mod in STATS]), buttons=BUTTON)

        
