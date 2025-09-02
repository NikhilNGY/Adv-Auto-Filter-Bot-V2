# (©) CodeFlix_Bots
# rohit_1888 on Tg # Dont remove this line

import base64
import re
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import OWNER_ID
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait
from database.database import db


# ✅ Check if user is admin (Owner also treated as admin)
async def check_admin(_, client, update):
    try:
        user_id = update.from_user.id
        return user_id == OWNER_ID or await db.admin_exist(user_id)
    except Exception as e:
        print(f"[!] Exception in check_admin: {e}")
        return False


# ✅ Check subscription for multiple channels
async def is_subscribed(client, user_id):
    channel_ids = await db.show_channels()

    if not channel_ids or user_id == OWNER_ID:
        return True

    for cid in channel_ids:
        if not await is_sub(client, user_id, cid):
            mode = await db.get_channel_mode(cid)
            if mode == "on":
                await asyncio.sleep(2)  # Allow join requests to process
                if await is_sub(client, user_id, cid):
                    continue
            return False
    return True


# ✅ Check subscription for single channel
async def is_sub(client, user_id, channel_id):
    try:
        member = await client.get_chat_member(channel_id, user_id)
        return member.status in {
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER
        }

    except UserNotParticipant:
        mode = await db.get_channel_mode(channel_id)
        if mode == "on":
            return await db.req_user_exist(channel_id, user_id)
        return False

    except Exception as e:
        print(f"[!] Error in is_sub(): {e}")
        return False


# ✅ Base64 encode/decode helpers
async def encode(string: str) -> str:
    return base64.urlsafe_b64encode(string.encode()).decode().strip("=")

async def decode(base64_string: str) -> str:
    base64_string = base64_string.strip("=")
    padded = base64_string + "=" * (-len(base64_string) % 4)
    return base64.urlsafe_b64decode(padded.encode()).decode()


# ✅ Fetch messages by ID
async def get_messages(client, message_ids):
    messages = []
    total_messages = 0

    while total_messages < len(message_ids):
        temp_ids = message_ids[total_messages:total_messages + 200]
        try:
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temp_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temp_ids
            )
        except Exception as e:
            print(f"[!] Error in get_messages: {e}")
            msgs = []
        total_messages += len(temp_ids)
        messages.extend(msgs)
    return messages


# ✅ Extract original message ID
async def get_message_id(client, message):
    if message.forward_from_chat:
        if message.forward_from_chat.id == client.db_channel.id:
            return message.forward_from_message_id
        return 0

    if message.forward_sender_name:
        return 0

    if message.text:
        pattern = r"https://t.me/(?:c/)?([^/]+)/(\d+)"
        matches = re.match(pattern, message.text)
        if not matches:
            return 0
        channel_id, msg_id = matches.groups()
        msg_id = int(msg_id)

        if channel_id.isdigit():
            return msg_id if f"-100{channel_id}" == str(client.db_channel.id) else 0
        return msg_id if channel_id == client.db_channel.username else 0

    return 0


# ✅ Human readable uptime
def get_readable_time(seconds: int) -> str:
    count, up_time, time_list = 0, "", []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for i, val in enumerate(time_list):
        time_list[i] = str(val) + time_suffix_list[i]

    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    return up_time + ":".join(time_list)


# ✅ Human readable expiry time
def get_exp_time(seconds: int) -> str:
    periods = [('days', 86400), ('hours', 3600), ('mins', 60), ('secs', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result += f'{int(period_value)} {period_name} '
    return result.strip()


# ✅ Filters
subscribed = filters.create(is_subscribed)
admin = filters.create(check_admin)
