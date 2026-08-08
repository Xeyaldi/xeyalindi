

import asyncio
import signal
import importlib
import fcntl
import sys
from contextlib import suppress

from xeyal import (anon, app, config, db, logger,
                   stop, thumb, userbot, yt)
from xeyal.plugins import all_modules


_lock_file = open("/tmp/xeyal_bot2.lock", "w")

def _acquire_single_instance_lock():
    try:
        fcntl.flock(_lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        logger.error("Bot artiq baska bir prosesde isleyir. Cixilir.")
        sys.exit(1)


async def idle():
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGABRT):
        with suppress(NotImplementedError):
            loop.add_signal_handler(sig, stop_event.set)
    await stop_event.wait()

async def main():
    await db.connect()
    await app.boot()
    await userbot.boot()
    await anon.boot()
    await thumb.start()

    for module in all_modules:
        importlib.import_module(f"xeyal.plugins.{module}")
    logger.info(f"Loaded {len(all_modules)} modules.")

    if config.COOKIES_URL:
        await yt.save_cookies(config.COOKIES_URL)

    sudoers = await db.get_sudoers()
    app.sudoers.update(sudoers)
    app.bl_users.update(await db.get_blacklisted())
    logger.info(f"Loaded {len(app.sudoers)} sudo users.")

    await idle()
    asyncio.create_task(stop())


if __name__ == "__main__":
    _acquire_single_instance_lock()
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
