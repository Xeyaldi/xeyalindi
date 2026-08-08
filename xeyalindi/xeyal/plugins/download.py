

import os
from collections import OrderedDict

from pyrogram import enums, filters, types

from xeyal import app, config, lang, logger, social, yt
from xeyal.helpers import Track, buttons, utils

_cache: "OrderedDict[str, Track]" = OrderedDict()
_CACHE_LIMIT = 300


def _remember(track: Track) -> None:
    _cache[track.id] = track
    _cache.move_to_end(track.id)
    if len(_cache) > _CACHE_LIMIT:
        _cache.popitem(last=False)


async def _show_format_choice(m: types.Message, url: str | None, query_text: str | None) -> None:
    """
    Shared flow for /indir /download and auto-detected YouTube links:
    looks the track up and shows the MP3/MP4 choice buttons.
    """
    sent = await m.reply_text(m.lang["indir_searching"], quote=True)

    if url:
        track = await yt.from_url(url, sent.id)
    else:
        track = await yt.search(query_text, sent.id)

    if not track or not track.id:
        return await sent.edit_text(
            m.lang["indir_not_found"].format(config.SUPPORT_CHAT)
        )

    if track.duration_sec and track.duration_sec > config.DURATION_LIMIT:
        return await sent.edit_text(
            m.lang["indir_duration_limit"].format(config.DURATION_LIMIT // 60)
        )

    _remember(track)
    await sent.edit_text(
        m.lang["indir_choose_format"].format(
            track.title or track.id,
            track.duration or "00:00",
            track.channel_name or "-",
        ),
        reply_markup=buttons.indir_format(track.id, m.from_user.id, m.lang),
    )


@app.on_message(filters.command(["indir", "download"]) & ~app.bl_users)
@lang.language()
async def _indir(_, m: types.Message):
    query_text = " ".join(m.command[1:]) if len(m.command) > 1 else None
    url = utils.get_url(m)
    if not url and query_text and yt.valid(query_text):
        url = query_text

    if not url and not query_text:
        return await m.reply_text(m.lang["indir_usage"], quote=True)

    await _show_format_choice(m, url, query_text if not url else None)


def _own_url(m: types.Message) -> str | None:
    """
    BU mesajin OZ linkine baxir, reply etdiyi mesaja yox. utils.get_url()
    reply olunan mesaji da yoxlayir - bu, bot muzik kartina (icinde mahninin
    youtube linki var) reply atib istenilen metn yazanda, o metni sehven
    "link paylasildi" kimi qebul edib avtomatik endirme basladirdi.
    """
    entities = m.entities or []
    text = m.text or ""
    for entity in entities:
        if entity.type == enums.MessageEntityType.TEXT_LINK:
            return entity.url
        if entity.type == enums.MessageEntityType.URL:
            return text[entity.offset : entity.offset + entity.length]
    return None


def _link_filter_func(_, __, m: types.Message) -> bool:
    text = m.text or ""
    if not text or text.startswith("/"):
        return False
    stripped = text.strip()
    if yt.valid(stripped):
        return True
    if _own_url(m):
        return True
    return bool(social.platform(text))


_link_filter = filters.create(_link_filter_func)


@app.on_message(_link_filter & ~app.bl_users, group=2)
@lang.language()
async def _auto_link_detect(_, m: types.Message):
    """
    Auto-detects a plain YouTube / Instagram / TikTok link pasted in a
    private chat or a group (no command needed) and starts the matching
    download flow automatically.
    """
    text = m.text or ""
    url = _own_url(m) or (text.strip() if yt.valid(text.strip()) else None)

    if url and yt.valid(url):
        return await _show_format_choice(m, url, None)

    platform = social.platform(text)
    if not platform:
        return

    link = social.extract_url(text, platform)
    if not link:
        return

    await _download_social(m, link, platform)


async def _download_social(m: types.Message, url: str, platform: str) -> None:
    sent = await m.reply_text(m.lang["social_downloading"], quote=True)
    try:
        result = await social.download(url, platform)
    except Exception as ex:
        logger.warning("social download failed: %s", ex)
        result = None

    if not result or not result.get("path") or not os.path.exists(result["path"]):
        return await sent.edit_text(
            m.lang["social_failed"].format(config.SUPPORT_CHAT)
        )

    await sent.edit_text(m.lang["social_uploading"])
    caption = m.lang["social_caption"].format(app.username)

    try:
        if result.get("photo"):
            await app.send_photo(
                chat_id=m.chat.id, photo=result["path"], caption=caption
            )
        else:
            await app.send_video(
                chat_id=m.chat.id,
                video=result["path"],
                caption=caption,
                supports_streaming=True,
            )
        await sent.delete()
    except Exception as ex:
        logger.warning("social upload failed: %s", ex)
        await sent.edit_text(m.lang["social_failed"].format(config.SUPPORT_CHAT))


@app.on_callback_query(filters.regex(r"^indir ") & ~app.bl_users)
@lang.language()
async def _indir_cb(_, query: types.CallbackQuery):
    data = query.data.split()
    action, video_id, uid = data[1], data[2], int(data[3])

    if query.from_user.id != uid:
        return await query.answer(query.lang["indir_not_yours"], show_alert=True)

    if action == "c":
        await query.answer()
        try:
            return await query.message.delete()
        except Exception:
            return

    await query.answer()
    video = action == "v"
    track = _cache.get(video_id)

    await query.edit_message_text(query.lang["indir_downloading"])
    try:
        file_path = await yt.download(video_id, video=video)
    except Exception as ex:
        logger.warning("indir download failed: %s", ex)
        file_path = None

    if not file_path or not os.path.exists(file_path):
        return await query.edit_message_text(query.lang["indir_failed"])

    await query.edit_message_text(query.lang["indir_uploading"])

    title = (track.title if track else video_id) or video_id
    channel = track.channel_name if track else None
    duration_sec = track.duration_sec if track else 0
    link = track.url if track else (yt.base + video_id)
    caption = query.lang["indir_caption"].format(title, app.username)
    markup = buttons.yt_key(link)

    sent_media = None
    try:
        if video:
            sent_media = await app.send_video(
                chat_id=query.message.chat.id,
                video=file_path,
                caption=caption,
                duration=duration_sec,
                supports_streaming=True,
                reply_markup=markup,
            )
        else:
            sent_media = await app.send_audio(
                chat_id=query.message.chat.id,
                audio=file_path,
                title=title[:60],
                performer=channel,
                duration=duration_sec,
                caption=caption,
                reply_markup=markup,
            )
        await query.message.delete()
    except Exception as ex:
        logger.warning("indir upload failed: %s", ex)
        return await query.edit_message_text(query.lang["indir_failed"])

    if config.SONG_LOG_ID and sent_media and not video:
        try:
            await sent_media.copy(
                chat_id=config.SONG_LOG_ID,
                caption=query.lang["song_log_caption"].format(
                    title,
                    query.from_user.mention,
                    query.message.chat.title or query.message.chat.first_name or "-",
                    link,
                ),
            )
        except Exception as ex:
            logger.warning("song log forward failed: %s", ex)
