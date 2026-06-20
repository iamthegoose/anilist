import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from anilist_bot.application.media_library_service import MediaLibraryService
from anilist_bot.application.settings import get_settings
from anilist_bot.infrastructure.storage.json_storage import JsonMediaRepository
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
    repository = JsonMediaRepository(settings.data_file)
    media_library = MediaLibraryService(repository, settings.fallback_image_url)

    dispatcher.include_router(build_router(media_library))
    dispatcher.startup.register(_set_webhook)
    dispatcher.shutdown.register(_delete_webhook)

    app = web.Application()
    app["bot"] = bot
    app["settings"] = settings
    SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        secret_token=settings.secret_token,
    ).register(app, path=settings.webhook_path)
    setup_application(app, dispatcher, bot=bot)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=settings.web_server_host, port=settings.web_server_port)
    await site.start()
    await asyncio.Event().wait()


async def _set_webhook(bot: Bot, **_: object) -> None:
    settings = get_settings()
    await bot.set_webhook(
        url=settings.webhook_url,
        secret_token=settings.secret_token,
        drop_pending_updates=True,
    )


async def _delete_webhook(bot: Bot, **_: object) -> None:
    await bot.delete_webhook(drop_pending_updates=False)


def main() -> None:
    try:
        asyncio.run(run())
    except RuntimeError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
