

from py_yt import VideosSearch
from pyrogram import types

from xeyal import app, config, db, lang
from xeyal.helpers import buttons
from xeyal.plugins.download import _cache, _remember
from xeyal.helpers import Track


def _track_result(track: Track, uid: int, _lang: dict) -> types.InlineQueryResultArticle:
    duration = track.duration or "00:00"
    channel = track.channel_name or "-"
    return types.InlineQueryResultArticle(
        id=track.id,
        title=track.title,
        description=f"{channel} • {duration}",
        thumb_url=track.thumbnail,
        input_message_content=types.InputTextMessageContent(
            _lang["km_fetching"]
        ),
    )


@app.on_inline_query()
async def _inline_search(_, iq: types.InlineQuery):
    query = (iq.query or "").strip()
    lang_code = await db.get_lang(iq.from_user.id)
    _lang = lang.languages[lang_code]

    if not query:
        recent = list(_cache.values())[-15:][::-1]
        results = [_track_result(t, iq.from_user.id, _lang) for t in recent]
        return await iq.answer(
            results,
            cache_time=1,
            switch_pm_text=_lang["indir_usage_inline"],
            switch_pm_parameter="start",
        )

    try:
        search = VideosSearch(query, limit=10, with_live=False)
        data = await search.next()
    except Exception:
        return await iq.answer([], cache_time=1)

    results = []
    for item in data.get("result", []):
        vid = item.get("id")
        if not vid:
            continue
        title = (item.get("title") or "Unknown")[:60]
        duration = item.get("duration") or "00:00"
        channel = item.get("channel", {}).get("name", "-")
        thumbs = item.get("thumbnails") or [{}]
        thumb = (thumbs[-1].get("url") or "").split("?")[0] or None
        link = item.get("link")

        track = Track(
            id=vid,
            channel_name=channel,
            duration=duration,
            duration_sec=0,
            message_id=0,
            title=title,
            thumbnail=thumb,
            url=link,
            view_count=item.get("viewCount", {}).get("short"),
            video=False,
        )
        _remember(track)
        results.append(_track_result(track, iq.from_user.id, _lang))

    await iq.answer(results, cache_time=30, is_personal=True)
