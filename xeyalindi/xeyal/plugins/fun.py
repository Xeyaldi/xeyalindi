

import hashlib

import aiohttp
from pyrogram import filters, types

from xeyal import app, lang, logger
from xeyal.helpers import utils

WAIFU_API = "https://api.waifu.pics/sfw/{action}"


async def _fetch_gif(action: str) -> str | None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(WAIFU_API.format(action=action), timeout=10) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                return data.get("url")
    except Exception as ex:
        logger.warning("fun gif fetch failed (%s): %s", action, ex)
        return None


async def _reaction(m: types.Message, action: str, lang_key: str) -> None:
    target = await utils.extract_user(m)
    if not target:
        return await m.reply_text(m.lang[f"{lang_key}_no_target"], quote=True)

    if target.id == m.from_user.id:
        return await m.reply_text(m.lang[f"{lang_key}_self"], quote=True)

    gif = await _fetch_gif(action)
    text = m.lang[f"{lang_key}_text"].format(m.from_user.mention, target.mention)

    if gif:
        try:
            return await m.reply_animation(gif, caption=text, quote=True)
        except Exception:
            pass
    await m.reply_text(text, quote=True)


@app.on_message(filters.command(["slap"]) & ~app.bl_users)
@lang.language()
async def _slap(_, m: types.Message):
    await _reaction(m, "slap", "slap")


@app.on_message(filters.command(["kiss"]) & ~app.bl_users)
@lang.language()
async def _kiss(_, m: types.Message):
    await _reaction(m, "kiss", "kiss")


@app.on_message(filters.command(["sevgi", "love"]) & ~app.bl_users)
@lang.language()
async def _sevgi(_, m: types.Message):
    target = await utils.extract_user(m)
    if not target:
        return await m.reply_text(m.lang["sevgi_no_target"], quote=True)

    if target.id == m.from_user.id:
        return await m.reply_text(m.lang["sevgi_self"], quote=True)

    pair_key = "-".join(sorted([str(m.from_user.id), str(target.id)]))
    digest = hashlib.md5(pair_key.encode()).hexdigest()
    percent = int(digest, 16) % 101

    if percent >= 80:
        tier = m.lang["sevgi_high"]
    elif percent >= 50:
        tier = m.lang["sevgi_mid"]
    else:
        tier = m.lang["sevgi_low"]

    await m.reply_text(
        m.lang["sevgi_text"].format(
            m.from_user.mention, target.mention, percent, tier
        ),
        quote=True,
    )
