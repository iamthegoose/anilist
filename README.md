# MediaList Telegram Bot

Telegram webhook bot for keeping a personal list of anime and movies.

## Features

- Runs through Telegram webhooks.
- Add anime or movies by sending plain text.
- Add anime or movies with an image by sending a photo and caption.
- Use bottom reply keyboard menus instead of inline message buttons.
- Switch interface language between Ukrainian and English.
- Add statuses and tags with hashtags.
- Use a fallback image URL when no photo is provided.
- Store entries locally in a JSON file.
- Show anime list, movie list, and stats.

## Setup

```bash
rye sync
cp .env.example .env
```

Fill `TELEGRAM_BOT_TOKEN` in `.env`, then run:

```bash
rye run bot
```

For webhooks, `.env` must include a public HTTPS URL:

```env
WEBHOOK_BASE_URL=https://your-domain.example
WEBHOOK_PATH=/telegram/webhook
WEB_SERVER_HOST=0.0.0.0
WEB_SERVER_PORT=8080
```

Run tests:

```bash
rye run test
```

## Commands

- `/start` - show intro and bottom menu.
- `/list` - show all saved media.
- `/help` - show available actions and tag format.

## Tags And Statuses

Add tags with `#` in the title or photo caption:

```text
Perfect Blue #watched #psychological
Inception #want #sci-fi
```

Supported status tags:

- Ukrainian: `#переглянуто`, `#хочу`, `#дивлюсь`, `#закинуто`
- English: `#watched`, `#want`, `#watching`, `#dropped`

## Project Structure

```text
src/anilist_bot/
  application/          use cases, settings, app-level services
  domain/               core models and repository contracts
  infrastructure/       JSON storage and future external integrations
  presentation/telegram Telegram router, handlers, and response formatting
    handlers/            one Telegram handler module per command/event group
  main.py               composition root and CLI entrypoint
tests/                  unit tests for services and storage
```
