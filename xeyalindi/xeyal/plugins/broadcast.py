

import os
import asyncio

from pyrogram import errors, filters, types

from xeyal import app, db, lang


broadcasting = asyncio.Lock()

DEAD_PEER_ERRORS = (
    errors.ChannelInvalid,
    errors.ChannelPrivate,
    errors.UserIsBlocked,
    errors.UserIsBot,
    errors.InputUserDeactivated,
    errors.ChatWriteForbidden,
)


async def _ensure_user_peer(user_id: int) -> None:
    """Bot bu user-i tanıyır (vaxtilə /start edib) amma lokal peer keşi
    itib - access_hash=0 ilə əl ilə storage-a yazıb yenidən sınayırıq."""
    try:
        await app.storage.update_peers([(user_id, 0, "user", None)])
    except Exception:
        pass


@app.on_message(filters.command(["broadcast"]) & app.sudoers)
@lang.language()
async def _broadcast(_, message: types.Message):
    if not message.reply_to_message:
        return await message.reply_text(message.lang["gcast_usage"])

    if broadcasting.locked():
        return await message.reply_text(message.lang["gcast_active"])

    msg = message.reply_to_message
    copy = "-copy" in message.command
    count, ucount, cleaned = 0, 0, 0
    groups, users = set(), set()
    sent = await message.reply_text(message.lang["gcast_start"])

    if "-nochat" not in message.command:
        groups = set(await db.get_chats())
    if "-nouser" not in message.command:
        users = set(await db.get_users())

    chats = list(groups) + list(users)
    failed = None

    async with broadcasting:
        for chat in chats:
            is_group = chat in groups
            for attempt in range(2):
                try:
                    (
                        await msg.copy(chat, reply_markup=msg.reply_markup)
                        if copy
                        else await msg.forward(chat)
                    )
                    if is_group:
                        count += 1
                    else:
                        ucount += 1
                    await asyncio.sleep(0.2)
                    break
                except errors.FloodWait as fw:
                    await asyncio.sleep(fw.value + 10)
                    continue
                except errors.PeerIdInvalid:
                    if not is_group and attempt == 0:
                        await _ensure_user_peer(chat)
                        continue
                    if not failed:
                        failed = open("errors.txt", "w")
                    failed.write(f"{chat} - PeerIdInvalid\n")
                    try:
                        await (db.rm_chat(chat) if is_group else db.rm_user(chat))
                        cleaned += 1
                    except Exception:
                        pass
                    break
                except DEAD_PEER_ERRORS as ex:
                    if not failed:
                        failed = open("errors.txt", "w")
                    failed.write(f"{chat} - {ex}\n")
                    try:
                        await (db.rm_chat(chat) if is_group else db.rm_user(chat))
                        cleaned += 1
                    except Exception:
                        pass
                    break
                except Exception as ex:
                    if not failed:
                        failed = open("errors.txt", "w")
                    failed.write(f"{chat} - {ex}\n")
                    break

    text = message.lang["gcast_end"].format(count, ucount)
    if cleaned:
        text += f"\n🧹 {cleaned} ölü chat/user bazadan silindi."
    if failed:
        failed.close()
        await message.reply_document(
            document="errors.txt",
            caption=text,
        )
        try: os.remove("errors.txt")
        except Exception: pass
        return

    await sent.edit_text(text)
