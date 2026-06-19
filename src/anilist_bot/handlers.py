from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from anilist_bot.models import AnimeEntry
from anilist_bot.storage import AnimeStorage


def build_router(storage: AnimeStorage, fallback_image_url: str) -> Router:
    router = Router()

    @router.message(Command("start"))
    async def start(message: Message) -> None:
        await message.answer(
            "Привіт. Надішли назву аніме текстом або фото з caption, і я додам його у список."
        )

    @router.message(Command("help"))
    async def help_command(message: Message) -> None:
        await message.answer(
            "Доступно:\n"
            "- текстове повідомлення: додати аніме без фото\n"
            "- фото з caption: додати аніме з фото\n"
            "- /list: показати список"
        )

    @router.message(Command("list"))
    async def list_entries(message: Message) -> None:
        entries = await storage.list_by_user(message.from_user.id)
        if not entries:
            await message.answer("Список поки порожній.")
            return

        lines = [f"{index}. {entry.title}" for index, entry in enumerate(entries, start=1)]
        await message.answer("Переглянуті аніме:\n" + "\n".join(lines))

    @router.message(F.photo)
    async def add_with_photo(message: Message) -> None:
        title = (message.caption or "").strip()
        if not title:
            await message.answer("Додай назву аніме в caption до фото.")
            return

        photo = message.photo[-1]
        await storage.add(
            AnimeEntry(
                user_id=message.from_user.id,
                title=title,
                image=photo.file_id,
                image_kind="telegram_file_id",
            )
        )
        await message.answer(f"Додав: {title}")

    @router.message(F.text)
    async def add_from_text(message: Message) -> None:
        title = message.text.strip()
        if title.startswith("/"):
            return

        await storage.add(
            AnimeEntry(
                user_id=message.from_user.id,
                title=title,
                image=fallback_image_url,
                image_kind="fallback_url",
            )
        )
        await message.answer(f"Додав: {title}")

    return router
