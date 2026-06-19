from aiogram import Router

from anilist_bot.application.anime_list_service import AnimeListService
from anilist_bot.presentation.telegram.handlers.add_anime import build_add_anime_router
from anilist_bot.presentation.telegram.handlers.help import build_help_router
from anilist_bot.presentation.telegram.handlers.list_anime import build_list_anime_router
from anilist_bot.presentation.telegram.handlers.start import build_start_router


def build_router(anime_lists: AnimeListService) -> Router:
    router = Router(name="telegram")
    router.include_router(build_start_router())
    router.include_router(build_help_router())
    router.include_router(build_list_anime_router(anime_lists))
    router.include_router(build_add_anime_router(anime_lists))
    return router
