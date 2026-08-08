
import os
import random

import aiohttp
from pyrogram import filters, types

from xeyal import app, config, lang

from xeyal.helpers._extra_data import BIO_QUOTES, SEVGI_QUOTES, ANIME_PHOTOS, PP_PHOTOS


@app.on_message(filters.command(["sevgi"]) & ~app.bl_users)
@lang.language()
async def sevgi_cmd(_, message: types.Message):
    await message.reply_text(random.choice(SEVGI_QUOTES), quote=True)


@app.on_message(filters.command(["bio"]) & ~app.bl_users)
@lang.language()
async def bio_cmd(_, message: types.Message):
    await message.reply_text(random.choice(BIO_QUOTES), quote=True)


@app.on_message(filters.command(["anime"]) & ~app.bl_users)
@lang.language()
async def anime_cmd(_, message: types.Message):
    photo = random.choice(ANIME_PHOTOS)
    await message.reply_photo(photo=photo, caption=message.lang["extra_anime_caption"].format(app.name))


@app.on_message(filters.command(["pp"]) & ~app.bl_users)
@lang.language()
async def pp_cmd(_, message: types.Message):
    photo = random.choice(PP_PHOTOS)
    await message.reply_photo(photo=photo, caption=message.lang["extra_pp_caption"].format(app.name))


async def _random_line(fname: str) -> str:
    with open(fname, "r", encoding="utf-8") as f:
        lines = [ln for ln in f.read().splitlines() if ln.strip()]
    return random.choice(lines)


@app.on_message(filters.command(["sehid"]) & ~app.bl_users)
@lang.language()
async def sehid_cmd(_, message: types.Message):
    try:
        line = await _random_line(config.SEHID_FILE)
    except FileNotFoundError:
        return await message.reply_text(message.lang["extra_sehid_missing"])
    await message.reply_text(f"🕯 {line}", quote=True)


@app.on_message(filters.command(["github"]) & ~app.bl_users)
@lang.language()
async def github_cmd(_, message: types.Message):
    if len(message.command) != 2:
        return await message.reply_text(message.lang["extra_github_usage"])

    username = message.command[1]
    url = f"https://api.github.com/users/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 404:
                return await message.reply_text(message.lang["extra_github_404"])
            data = await resp.json()

    caption = message.lang["extra_github_card"].format(
        name=data.get("name") or username,
        username=username,
        bio=data.get("bio") or "-",
        url=data.get("html_url"),
        company=data.get("company") or "-",
        created_at=data.get("created_at"),
        repos=data.get("public_repos"),
        blog=data.get("blog") or "-",
        location=data.get("location") or "-",
        followers=data.get("followers"),
        following=data.get("following"),
    )
    avatar = data.get("avatar_url")
    if avatar:
        await message.reply_photo(photo=avatar, caption=caption)
    else:
        await message.reply_text(caption)


@app.on_message(filters.command(["tgm"]) & ~app.bl_users)
@lang.language()
async def telegraph_cmd(client, message: types.Message):
    replied = message.reply_to_message
    supported = replied and (
        (replied.photo and replied.photo.file_size <= 5242880)
        or (replied.animation and replied.animation.file_size <= 5242880)
        or (replied.video and replied.video.file_size <= 5242880)
    )
    if not supported:
        return await message.reply_text(message.lang["extra_tgm_usage"])

    path = await client.download_media(replied)
    try:
        from telegraph import upload_file

        result = upload_file(path)
        link = f"https://telegra.ph{result[0]}"
        await message.reply_text(
            message.lang["extra_tgm_done"].format(link, app.name),
            disable_web_page_preview=False,
        )
    except Exception as e:
        await message.reply_text(message.lang["extra_tgm_fail"].format(e))
    finally:
        if path and os.path.exists(path):
            os.remove(path)
