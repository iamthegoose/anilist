import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from anilist_bot.config import get_settings
from anilist_bot.handlers import build_router
from anilist_bot.storage import AnimeStorage


async def run() -> None:
    settings = get_settings()
    settings.validate_ready()

    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    bot = Bot(token=settings.token)
    dispatcher = Dispatcher()
    storage = AnimeStorage(settings.data_file)

    dispatcher.include_router(build_router(storage, settings.fallback_image_url))
    await dispatcher.start_polling(bot)


def main() -> None:
    try:
        asyncio.run(run())
    except RuntimeError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
