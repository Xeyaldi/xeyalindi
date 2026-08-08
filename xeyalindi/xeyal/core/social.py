

import os
import re
import random
import asyncio
import hashlib
from pathlib import Path

import yt_dlp

from xeyal import logger


class Social:
    """
    Generic downloader for Instagram and TikTok links using yt-dlp.
    Unlike YouTube, these platforms don't need a format choice: we always
    grab the best available video (or photo, for Instagram image posts).
    """

    def __init__(self):
        self.instagram = re.compile(
            r"https?://(?:www\.)?instagram\.com/(?:[^/]+/)?"
            r"(?:p|reel|reels|tv)/[A-Za-z0-9_-]+"
        )
        self.tiktok = re.compile(
            r"https?://(?:(?:www|vm|vt|m)\.)?tiktok\.com/\S+"
        )
        self.cookie_dir = "xeyal/cookies"

    def get_cookies(self, platform: str) -> str | None:
        if not os.path.isdir(self.cookie_dir):
            return None
        matches = [
            f for f in os.listdir(self.cookie_dir)
            if f.lower().endswith(".txt") and platform in f.lower()
        ]
        if not matches:
            return None
        return os.path.join(self.cookie_dir, random.choice(matches))

    def platform(self, text: str) -> str | None:
        if not text:
            return None
        if self.tiktok.search(text):
            return "tiktok"
        if self.instagram.search(text):
            return "instagram"
        return None

    def extract_url(self, text: str, kind: str) -> str | None:
        pattern = self.tiktok if kind == "tiktok" else self.instagram
        match = pattern.search(text)
        return match.group(0) if match else None

    async def download(self, url: str, platform: str) -> dict | None:
        """
        Downloads media from the given url.
        Returns a dict: {"path": str, "photo": bool, "title": str} or None.
        """
        uid = hashlib.md5(url.encode()).hexdigest()[:16]
        outtmpl = f"downloads/social_{uid}.%(ext)s"

        ydl_opts = {
            "outtmpl": outtmpl,
            "quiet": True,
            "no_warnings": True,
            "nocheckcertificate": True,
            "geo_bypass": True,
            "format": "bestvideo+bestaudio/best/best",
            "merge_output_format": "mp4",
        }

        cookiefile = self.get_cookies(platform)
        if cookiefile:
            ydl_opts["cookiefile"] = cookiefile

        def _download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(url, download=True)
                except Exception as ex:
                    logger.warning("Social download failed (%s): %s", platform, ex)
                    return None

                if not info:
                    return None

                path = ydl.prepare_filename(info)
                if not Path(path).exists():
                    matches = list(Path("downloads").glob(f"social_{uid}.*"))
                    if not matches:
                        return None
                    path = str(matches[0])

                photo = Path(path).suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")
                return {
                    "path": path,
                    "photo": photo,
                    "title": (info.get("title") or info.get("description") or "")[:60],
                }

        return await asyncio.to_thread(_download)
