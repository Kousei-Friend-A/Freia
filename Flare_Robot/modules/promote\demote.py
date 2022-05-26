import os
import html

from telegram import ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async
from telegram.utils.helpers import mention_html
from telethon import events
from telethon.tl import functions, types

from Flare_Robot import DRAGONS, dispatcher, INFOPIC, telethn as bot
from Flare_Robot.modules.disable import DisableAbleCommandHandler
from Flare_Robot.modules.helper_funcs.chat_status import (
    bot_admin,
    can_pin,
    can_promote,
    connection_status,
    user_admin,
    user_can_changeinfo,
    user_can_pin,
    user_can_promote,
    ADMIN_CACHE,
)

from Flare_Robot.modules.helper_funcs.extraction import (
    extract_user,
    extract_user_and_text,
)
from Flare_Robot.modules.log_channel import loggable
from Flare_Robot.modules.helper_funcs.alternate import send_message

BUTTON = [
        [
            Button.url("📢 User", "user_member.user.id, user_member.user.first_name"),
            Button.url("🚑 By Admin", "user.id, user.first_name"),
        ]
    ]

async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await bot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True
    
async def can_promote_users(message):
    result = await bot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )

async def can_ban_users(message):
    result = await bot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )

        
@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def ppromote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    promoter = chat.get_member(user.id)

    if (
        not (promoter.can_promote_members or promoter.status == "creator")
        and user.id not in DRAGONS
    ):
        message.reply_text("You don't have the necessary rights to do that!")
        return

    user_id = extract_user(message, args)

    if not user_id:
        message.reply_text(
            "You don't seem to be referring to a user or the ID specified is incorrect..",
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status in ('administrator', 'creator'):
        message.reply_text("How am I meant to promote someone that's already an admin?")
        return

    if user_id == bot.id:
        message.reply_text("I can't promote myself! Get an admin to do it for me.")
        return

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=bot_member.can_change_info,
            can_post_messages=bot_member.can_post_messages,
            can_edit_messages=bot_member.can_edit_messages,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            # can_promote_members=bot_member.can_promote_members,
            can_restrict_members=bot_member.can_restrict_members,
            can_pin_messages=bot_member.can_pin_messages,
        )
    except BadRequest as err:
        if err.message == "User_not_mutual_contact":
            message.reply_text("I can't promote someone who isn't in the group.")
        else:
            message.reply_text("An error occured while promoting.")
        return

    TEXT = "#SUCCESSFULLY PROMOTED"

    bot.send_message(event.chat_id, caption=TEXT, buttons=BUTTON)


    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#PROMOTED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
    )

    return log_message



__help__ = """
*Promote & Demote Commands are Admins only*:
  ➢ `/promote (user) (?admin's title)`*:* Promotes the user to admin.
  ➢ `/demote (user)`*:* Demotes the user from admin.
  ➢ `/lowpromote`*:* Promote a member with low rights
  ➢ `/midpromote`*:* Promote a member with Middium rights
  ➢ `/fullpromote`*:* Promote a member with full rights
  ➢ `/lowdemote`*:* Demote an admin to low
  ➢ `/middemote`*:* Demote an admin to middium
"""


PPROMOTE_HANDLER = DisableAbleCommandHandler("ppromote", ppromote, run_async=True)
FFULLPROMOTE_HANDLER = DisableAbleCommandHandler("ffullpromote", ffullpromote, run_async=True)
LOW_PROMOTE_HANDLER = DisableAbleCommandHandler("lowpromote", lowpromote, run_async=True)
MID_PROMOTE_HANDLER = DisableAbleCommandHandler("midpromote", midpromote, run_async=True)
DDEMOTE_HANDLER = DisableAbleCommandHandler("ddemote", ddemote, run_async=True)
SET_TTITLE_HANDLER = CommandHandler("ttitle", set_ttitle, run_async=True)

dispatcher.add_handler(PPROMOTE_HANDLER)
dispatcher.add_handler(FFULLPROMOTE_HANDLER)
dispatcher.add_handler(LOW_PROMOTE_HANDLER)
dispatcher.add_handler(MID_PROMOTE_HANDLER)
dispatcher.add_handler(DDEMOTE_HANDLER)
dispatcher.add_handler(SET_TTITLE_HANDLER)

__mod_name__ = "Admins"
__command_list__ = [
    "promote", 
    "fullpromote",
    "lowpromote",
    "midpromote",
    "demote",
    "title",
    "promote",
]
__handlers__ = [
    PPROMOTE_HANDLER,
    FFULLPROMOTE_HANDLER,
    LOW_PROMOTE_HANDLER,
    MID_PROMOTE_HANDLER,
    DDEMOTE_HANDLER,
    SET_TTITLE_HANDLER,
]
