

from pyrogram import types

from xeyal import app, config, lang
from xeyal.core.lang import lang_codes


class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

    def cancel_dl(self, text) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=text, callback_data=f"cancel_dl")]])

    def controls(
        self,
        chat_id: int,
        status: str = None,
        timer: str = None,
        remove: bool = False,
        _lang: dict = None,
    ) -> types.InlineKeyboardMarkup:
        keyboard = []
        if status:
            keyboard.append(
                [self.ikb(text=status, callback_data=f"controls status {chat_id}")]
            )

        if _lang:
            keyboard.append(
                [
                    self.ikb(
                        text=_lang["add_me"],
                        url=f"https://t.me/{app.username}?startgroup=true",
                    )
                ]
            )
            keyboard.append(
                [
                    self.ikb(text=_lang["channel"], url=config.SUPPORT_CHANNEL),
                    self.ikb(text=_lang["support"], url=config.SUPPORT_CHAT),
                ]
            )
            keyboard.append(
                [
                    self.ikb(
                        text=_lang["close"],
                        callback_data=f"controls close {chat_id}",
                    )
                ]
            )
        return self.ikm(keyboard)

    def help_markup(
        self, _lang: dict, back: bool = False, from_start: bool = False
    ) -> types.InlineKeyboardMarkup:
        if back:
            rows = [
                [
                    self.ikb(text=_lang["back"], callback_data="help back"),
                    self.ikb(text=_lang["close"], callback_data="help close"),
                ]
            ]
        else:
            cbs = ["admins", "auth", "blist", "lang", "ping", "play", "queue", "stats", "sudo", "dl", "games", "tag", "fun", "extra", "edu"]
            buttons = [
                self.ikb(text=_lang[f"help_{i}"], callback_data=f"help {cb}")
                for i, cb in enumerate(cbs)
            ]
            rows = [buttons[i : i + 3] for i in range(0, len(buttons), 3)]
            if from_start:
                rows.append(
                    [self.ikb(text=_lang["back"], callback_data="help start_back")]
                )

        return self.ikm(rows)

    def lang_markup(self, _lang: str) -> types.InlineKeyboardMarkup:
        langs = lang.get_languages()

        buttons = [
            self.ikb(
                text=f"{name} ({code}) {'✔️' if code == _lang else ''}",
                callback_data=f"lang_change {code}",
            )
            for code, name in langs.items()
        ]
        rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        return self.ikm(rows)

    def ping_markup(self, text: str) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=text, url=config.SUPPORT_CHAT)]])

    def play_queued(
        self, chat_id: int, item_id: str, _text: str
    ) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text=_text, callback_data=f"controls force {chat_id} {item_id}"
                    )
                ]
            ]
        )

    def queue_markup(
        self, chat_id: int, _text: str, playing: bool
    ) -> types.InlineKeyboardMarkup:
        _action = "pause" if playing else "resume"
        return self.ikm(
            [[self.ikb(text=_text, callback_data=f"controls {_action} {chat_id} q")]]
        )

    def settings_markup(
        self, lang: dict, admin_only: bool, cmd_delete: bool, language: str, chat_id: int
    ) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text=lang["play_mode"] + " ➜",
                        callback_data="settings",
                    ),
                    self.ikb(text=admin_only, callback_data="settings play"),
                ],
                [
                    self.ikb(
                        text=lang["cmd_delete"] + " ➜",
                        callback_data="settings",
                    ),
                    self.ikb(text=cmd_delete, callback_data="settings delete"),
                ],
                [
                    self.ikb(
                        text=lang["language"] + " ➜",
                        callback_data="settings",
                    ),
                    self.ikb(text=lang_codes[language], callback_data="language"),
                ],
            ]
        )

    def start_key(
        self, lang: dict, private: bool = False
    ) -> types.InlineKeyboardMarkup:
        rows = [
            [
                self.ikb(
                    text=lang["add_me"],
                    url=f"https://t.me/{app.username}?startgroup=true",
                )
            ],
            [
                self.ikb(text=lang["support"], url=config.SUPPORT_CHAT),
                self.ikb(text=lang["channel"], url=config.SUPPORT_CHANNEL),
            ],
            [
                self.ikb(text=lang["source"], url="https://t.me/kullaniciadidi"),
                self.ikb(text=lang["help"], callback_data="help"),
            ],
        ]
        return self.ikm(rows)

    def indir_format(self, video_id: str, uid: int, _lang: dict) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text=_lang["indir_btn_mp3"],
                        callback_data=f"indir a {video_id} {uid}",
                    ),
                    self.ikb(
                        text=_lang["indir_btn_mp4"],
                        callback_data=f"indir v {video_id} {uid}",
                    ),
                ],
                [
                    self.ikb(
                        text=_lang["indir_btn_cancel"],
                        callback_data=f"indir c {video_id} {uid}",
                    )
                ],
            ]
        )

    def km_format(self, video_id: str, uid: int, _lang: dict) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text=_lang["km_btn_get"],
                        callback_data=f"kminline g {video_id} {uid}",
                    )
                ],
                [
                    self.ikb(
                        text=_lang["indir_btn_cancel"],
                        callback_data=f"kminline c {video_id} {uid}",
                    )
                ],
            ]
        )

    def games_menu(self) -> types.InlineKeyboardMarkup:
        rows = [
            [
                self.ikb(text="🎲", callback_data="game dice"),
                self.ikb(text="🎯", callback_data="game dart"),
                self.ikb(text="🏀", callback_data="game basket"),
            ],
            [
                self.ikb(text="⚽", callback_data="game football"),
                self.ikb(text="🎳", callback_data="game bowl"),
                self.ikb(text="🎰", callback_data="game slot"),
            ],
        ]
        return self.ikm(rows)

    def yt_key(self, link: str) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(text="❐", copy_text=link),
                    self.ikb(text="Youtube", url=link),
                ],
            ]
                )
