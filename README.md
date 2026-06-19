# AniList Telegram Bot

Telegram bot for keeping a personal list of watched anime.

## Features

- Add watched anime by sending plain text.
- Add watched anime with an image by sending a photo and caption.
- Use a fallback image URL when no photo is provided.
- Store entries locally in a JSON file.
- Show your list with `/list`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Fill `TELEGRAM_BOT_TOKEN` in `.env`, then run:

```bash
anilist-bot
```

## Commands

- `/start` - show a short intro.
- `/list` - show watched anime.
- `/help` - show available actions.

