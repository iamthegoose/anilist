from aiogram import Router

from anilist_bot.application.media_library_service import MediaLibraryService
from anilist_bot.presentation.telegram.handlers.add_media import build_add_media_router
from anilist_bot.presentation.telegram.handlers.help import build_help_router
from anilist_bot.presentation.telegram.handlers.list_media import build_list_media_router
from anilist_bot.presentation.telegram.handlers.menu import build_menu_router
from anilist_bot.presentation.telegram.handlers.start import build_start_router


def build_router(media_library: MediaLibraryService) -> Router:
    router = Router(name="telegram")
    router.include_router(build_start_router(media_library))
    router.include_router(build_help_router(media_library))
    router.include_router(build_menu_router(media_library))
    router.include_router(build_list_media_router(media_library))
    router.include_router(build_add_media_router(media_library))
    return router
