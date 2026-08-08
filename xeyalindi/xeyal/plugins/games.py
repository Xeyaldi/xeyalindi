

from pyrogram import filters, types

from xeyal import app, lang
from xeyal.helpers import buttons

GAME_EMOJI = {
    "dice": "🎲",
    "dart": "🎯",
    "basket": "🏀",
    "football": "⚽",
    "bowl": "🎳",
    "slot": "🎰",
}


@app.on_message(filters.command(["games", "oyunlar", "oyun"]) & ~app.bl_users)
@lang.language()
async def _games(_, m: types.Message):
    await m.reply_text(
        m.lang["games_menu_text"], reply_markup=buttons.games_menu(), quote=True
    )


@app.on_callback_query(filters.regex(r"^game ") & ~app.bl_users)
@lang.language()
async def _games_cb(_, query: types.CallbackQuery):
    key = query.data.split()[1]
    emoji = GAME_EMOJI.get(key)
    if not emoji:
        return await query.answer()

    await query.answer()
    dice_msg = await app.send_dice(chat_id=query.message.chat.id, emoji=emoji)
    value = dice_msg.dice.value if dice_msg.dice else "-"
    await dice_msg.reply_text(
        query.lang["games_result"].format(query.from_user.mention, value),
        quote=True,
    )
