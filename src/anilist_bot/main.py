import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from anilist_bot.application.anime_list_service import AnimeListService
from anilist_bot.application.settings import get_settings
from anilist_bot.infrastructure.storage.json_storage import JsonAnimeRepository
from anilist_bot.presentation.telegram.router import build_router


async def run() -> None:
    settings = get_settings()
    settings.validate_ready()

    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    bot = Bot(
        token=settings.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()
    repository = JsonAnimeRepository(settings.data_file)
    anime_lists = AnimeListService(repository, settings.fallback_image_url)

    dispatcher.include_router(build_router(anime_lists))
    await dispatcher.start_polling(bot)


def main() -> None:
    try:
        asyncio.run(run())
    except RuntimeError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
