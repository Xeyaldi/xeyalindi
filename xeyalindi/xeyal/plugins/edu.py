
import json
import os
import time

import aiohttp
from pyrogram import filters, types

from xeyal import app, config, lang

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
PEXELS_IMAGE_URL = "https://api.pexels.com/v1/search"
PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"


def _load_catalog() -> list:
    try:
        with open(config.CATALOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save_catalog(items: list) -> None:
    os.makedirs(os.path.dirname(config.CATALOG_PATH) or ".", exist_ok=True)
    with open(config.CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


@app.on_message(filters.command(["ask"]) & ~app.bl_users)
@lang.language()
async def ask_cmd(_, message: types.Message):
    if not config.GROQ_API_KEY:
        return await message.reply_text(message.lang["edu_no_groq_key"])

    if len(message.command) < 2:
        return await message.reply_text(message.lang["edu_ask_usage"])

    question = message.text.split(None, 1)[1]
    wait = await message.reply_text(message.lang["edu_ask_thinking"], quote=True)

    payload = {
        "model": config.GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Sən Azərbaycan dilində, qısa və aydın cavab verən köməkçi "
                    "AI-san. Tələbələrə təhsil mövzularında kömək edirsən."
                ),
            },
            {"role": "user", "content": question},
        ],
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.GROQ_API_KEY}",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(GROQ_URL, json=payload, headers=headers, timeout=30) as resp:
                data = await resp.json()
        if "error" in data:
            return await wait.edit_text(message.lang["edu_groq_error"].format(data["error"].get("message")))
        answer = data["choices"][0]["message"]["content"]
    except Exception as e:
        return await wait.edit_text(message.lang["edu_groq_error"].format(e))

    await wait.edit_text(answer)


async def _pexels_get(endpoint: str, query: str, per_page: int):
    if not config.PEXELS_API_KEY:
        return None
    headers = {"Authorization": config.PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page}
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint, params=params, headers=headers, timeout=20) as resp:
            return await resp.json()


@app.on_message(filters.command(["img"]) & ~app.bl_users)
@lang.language()
async def pexels_image_cmd(_, message: types.Message):
    if not config.PEXELS_API_KEY:
        return await message.reply_text(message.lang["edu_no_pexels_key"])
    if len(message.command) < 2:
        return await message.reply_text(message.lang["edu_img_usage"])

    query = message.text.split(None, 1)[1]
    data = await _pexels_get(PEXELS_IMAGE_URL, query, 5)
    photos = (data or {}).get("photos", [])
    if not photos:
        return await message.reply_text(message.lang["edu_no_results"])

    urls = [p["src"]["large"] for p in photos]
    media = [types.InputMediaPhoto(u) for u in urls]
    await message.reply_media_group(media)


@app.on_message(filters.command(["vid"]) & ~app.bl_users)
@lang.language()
async def pexels_video_cmd(_, message: types.Message):
    if not config.PEXELS_API_KEY:
        return await message.reply_text(message.lang["edu_no_pexels_key"])
    if len(message.command) < 2:
        return await message.reply_text(message.lang["edu_vid_usage"])

    query = message.text.split(None, 1)[1]
    data = await _pexels_get(PEXELS_VIDEO_URL, query, 3)
    videos = (data or {}).get("videos", [])
    if not videos:
        return await message.reply_text(message.lang["edu_no_results"])

    best = videos[0]["video_files"][-1]["link"]
    await message.reply_video(best)


@app.on_message(filters.command(["catalog"]) & ~app.bl_users)
@lang.language()
async def catalog_cmd(_, message: types.Message):
    items = _load_catalog()
    if len(message.command) > 1:
        needle = message.text.split(None, 1)[1].lower()
        items = [
            i for i in items
            if needle in i.get("title", "").lower() or needle in i.get("keywords", "").lower()
        ]

    if not items:
        return await message.reply_text(message.lang["edu_catalog_empty"])

    for item in items[:10]:
        try:
            await message.reply_document(
                item["file_id"],
                caption=message.lang["edu_catalog_item"].format(item["title"], item.get("category", "-")),
            )
        except Exception:
            continue


def _is_admin(user_id: int) -> bool:
    return user_id == config.OWNER_ID or user_id in config.ADMIN_IDS


@app.on_message(filters.command(["addfile"]) & filters.reply & ~app.bl_users)
@lang.language()
async def addfile_cmd(_, message: types.Message):
    if not _is_admin(message.from_user.id):
        return await message.reply_text(message.lang["edu_not_admin"])

    doc = message.reply_to_message.document
    if not doc:
        return await message.reply_text(message.lang["edu_addfile_usage"])

    if len(message.command) < 3:
        return await message.reply_text(message.lang["edu_addfile_usage"])

    category = message.command[1]
    rest = message.text.split(None, 2)[2]
    title, _, keywords = rest.partition("|")

    items = _load_catalog()
    items.append(
        {
            "id": str(int(time.time() * 1000)),
            "title": title.strip(),
            "keywords": keywords.strip(),
            "file_id": doc.file_id,
            "category": category,
            "added_by": message.from_user.id,
            "added_at": int(time.time()),
        }
    )
    _save_catalog(items)
    await message.reply_text(message.lang["edu_addfile_done"].format(title.strip()))
