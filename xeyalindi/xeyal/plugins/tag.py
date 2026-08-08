
import asyncio
import random
from pyrogram import filters, types
from pyrogram.enums import ParseMode

from xeyal import app, lang
from xeyal.helpers import admin_check

active_tags = {}

FLAGS = [
    "🇦🇿", "🇹🇷", "🇵🇰", "🇺🇸", "🇬🇧", "🇩🇪", "🇫🇷", "🇮🇹", "🇷🇺", "🇪🇸",
    "🇺🇦", "🇧🇷", "🇦🇷", "🇨🇦", "🇯🇵", "🇨🇳", "🇰🇷", "🇸🇦", "🇦🇪", "🇶🇦",
    "🇪🇬", "🇮🇳", "🇮🇩", "🇲🇾", "🇮🇷", "🇮🇶", "🇮🇪", "🇳🇱", "🇧🇪", "🇨🇭",
    "🇸🇪", "🇳🇴", "🇫🇮", "🇩🇰", "🇵🇱", "🇵🇹", "🇬🇷", "🇿🇦", "🇲🇽", "🇨🇱",
    "🇨🇴", "🇦🇺", "🇳🇿", "🇰🇿", "🇺🇿", "🇹🇲", "🇰🇬", "🇹🇯", "🇬🇪", "🇲🇩",
    "🇧🇬", "🇷🇴", "🇭ũ", "🇦🇹", "🇧🇪", "🇨🇿", "🇭🇷", "🇷🇸", "🇦🇱", "🇲🇪",
    "🇲🇦", "🇩🇿", "🇹🇳", "🇱🇾", "🇸🇩", "🇱🇧", "🇯🇴", "🇸🇾", "🇰🇼", "🇴🇲"
]

@app.on_message(
    filters.command(["tag", "tektag", "bayragtag", "bayraktag"]) & filters.group & ~app.bl_users
)
@lang.language()
@admin_check
async def tag_all(_, m: types.Message):
    chat_id = m.chat.id
    
    if active_tags.get(chat_id):
        return await m.reply_text("Bu qrupda onsuz da aktiv tağ prosesi var!", quote=True)
        
    command = m.command[0].lower()
    custom_text = " ".join(m.command[1:]) if len(m.command) > 1 else None

    current_chunk_size = 1 if command == "tektag" else 5

    tagged = []
    async for member in app.get_chat_members(chat_id):
        if member.user.is_bot or member.user.is_deleted:
            continue
        
        first_name = member.user.first_name.replace("<", "&lt;").replace(">", "&gt;") if member.user.first_name else "User"
        mention = f'<a href="tg://user?id={member.user.id}">{first_name}</a>'
        
        if command in ["bayragtag", "bayraktag"]:
            tagged.append(f"{random.choice(FLAGS)} {mention}")
        else:
            tagged.append(mention)

    if not tagged:
        return await m.reply_text(m.lang["tag_no_members"], quote=True)

    header = (
        m.lang["tag_header_custom"].format(custom_text)
        if custom_text
        else m.lang["tag_header"]
    )

    active_tags[chat_id] = True

    for i in range(0, len(tagged), current_chunk_size):
        if not active_tags.get(chat_id):
            break
            
        chunk = tagged[i : i + current_chunk_size]
        separator = "\n" if command in ["bayragtag", "bayraktag"] else " "
        
        text = header + "\n\n" + separator.join(chunk)
        
        try:
            await app.send_message(
                chat_id=chat_id,
                text=text,
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML
            )
            await asyncio.sleep(1.7)
        except Exception:
            pass

    active_tags[chat_id] = False

    try:
        await m.delete()
    except Exception:
        pass


@app.on_message(
    filters.command(["tagstop", "stop"]) & filters.group & ~app.bl_users
)
@admin_check
async def stop_tagging(_, m: types.Message):
    chat_id = m.chat.id
    
    if active_tags.get(chat_id):
        active_tags[chat_id] = False
        await m.reply_text("Tağ prosesi admin tərəfindən uğurla dayandırıldı. ✅", quote=True)
    else:
        await m.reply_text("Bu qrupda onsuz da aktiv işləyən tağ yoxdur. ❌", quote=True)
