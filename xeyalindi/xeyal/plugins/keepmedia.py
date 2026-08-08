
import asyncio

from pyrogram import types

from xeyal import app, config, db, lang, logger, userbot
from xeyal.plugins.download import _cache


async def _fetch_from_keepmedia(query_text: str) -> types.Message | None:
    client = userbot.one

    results = await client.get_inline_bot_results(config.KEEPMEDIA_BOT, query_text)
    if not results or not results.results:
        return None

    chosen = None
    for r in results.results:
        rtype = (getattr(r, "type", "") or "").lower()
        if "audio" in rtype or "voice" in rtype or "document" in rtype:
            chosen = r
            break
    chosen = chosen or results.results[0]

    before_id = 0
    try:
        async for last in client.get_chat_history(config.KEEPMEDIA_DUMP_CHAT, limit=1):
            before_id = last.id
    except Exception:
        pass

    await client.send_inline_bot_result(
        chat_id=config.KEEPMEDIA_DUMP_CHAT,
        query_id=results.query_id,
        result_id=chosen.id,
    )

    for _ in range(6):
        await asyncio.sleep(1.5)
        async for m in client.get_chat_history(config.KEEPMEDIA_DUMP_CHAT, limit=5):
            if m.id <= before_id:
                break
            if m.audio or m.voice or m.document:
                return m
    return None


@app.on_chosen_inline_result()
async def _chosen_result(_, cir: types.ChosenInlineResult):
    if not cir.inline_message_id:
        logger.warning(
            "Chosen inline result has no inline_message_id — "
            "enable /setinlinefeedback 100%% for this bot in @BotFather."
        )
        return

    lang_code = await db.get_lang(cir.from_user.id)
    _lang = lang.languages[lang_code]

    track = _cache.get(cir.result_id)
    title = track.title if track else cir.result_id
    search_text = f"{title} {track.channel_name}" if track and track.channel_name else title

    try:
        msg = await _fetch_from_keepmedia(search_text)
    except Exception as ex:
        logger.warning("KeepMediaBot fetch failed: %s", ex)
        try:
            await app.edit_inline_text(cir.inline_message_id, _lang["km_failed"])
        except Exception:
            pass
        return

    media = msg and (msg.audio or msg.voice or msg.document)
    if not media:
        try:
            await app.edit_inline_text(cir.inline_message_id, _lang["km_not_found"])
        except Exception:
            pass
        return

    caption = _lang["indir_caption"].format(title, app.username)
    try:
        await app.edit_inline_media(
            cir.inline_message_id, types.InputMediaAudio(media.file_id, caption=caption)
        )
    except Exception as ex:
        logger.warning("KeepMediaBot inline media edit failed, falling back: %s", ex)
        try:
            await app.edit_inline_media(
                cir.inline_message_id, types.InputMediaDocument(media.file_id, caption=caption)
            )
        except Exception as ex2:
            logger.warning("KeepMediaBot inline fallback also failed: %s", ex2)
            try:
                await app.edit_inline_text(cir.inline_message_id, _lang["km_failed"])
            except Exception:
                pass
