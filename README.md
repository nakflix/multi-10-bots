# Multi-Bot File Sharing - Deploy up to 10 Bots

This codebase runs **up to 10 Telegram bots** from a single deployment/process.
All 10 bots share the exact same configuration (force-sub channels, admins,
DB storage channel, captions, etc.) — only 3 things differ per bot:

1. **Bot Token** (`BOT{N}_TOKEN`)
2. **MongoDB URI** (`BOT{N}_DB_URI`)
3. **MongoDB Database Name** (`BOT{N}_DB_NAME`)

Each bot keeps its own isolated user list (own MongoDB collection), so
`/broadcast`, `/pin`, `/unpin`, and `/users` only affect that specific bot's
own subscribers.

## Setup

1. Copy `.env.example` to `.env`
2. Fill in the **shared settings** at the top (same for every bot)
3. Fill in `BOT1_TOKEN`, `BOT1_DB_URI`, `BOT1_DB_NAME` through as many slots
   (up to `BOT10_*`) as bots you want running. Any slot left with an empty
   `TOKEN` is simply skipped — so you can run 1, 5, or all 10 bots.

```env
BOT1_TOKEN=123456:AAExampleToken1
BOT1_DB_URI=mongodb+srv://user:pass@cluster1.mongodb.net
BOT1_DB_NAME=bot1_db

BOT2_TOKEN=789012:AAExampleToken2
BOT2_DB_URI=mongodb+srv://user:pass@cluster1.mongodb.net
BOT2_DB_NAME=bot2_db
```

> You can point all bots at the **same MongoDB cluster** — just give each a
> different `DB_NAME` so their user lists don't collide.

## Run locally

```bash
pip install -r requirements.txt
python3 main.py
```

All configured bots start concurrently in a single process and stay running.
Each bot's web/health-check server binds to its own port automatically
(`PORT`, `PORT+1`, `PORT+2`, ... up to `PORT+9`), so port conflicts are
avoided even with all 10 running together.

## Deploy with Docker

```bash
docker build -t multibot .
docker run --env-file .env -p 8080-8089:8080-8089 multibot
```

## Deploy on Heroku / similar PaaS

The `Procfile` and `app.json` work as-is — set all the `BOT{N}_*` and shared
env vars in your dashboard, same as the `.env.example` layout.

## Important notes

- **CHANNEL_ID, FORCE_SUB_CHANNEL_1-4, ADMINS, OWNER_ID** are shared across
  all bots. Make sure **every bot** is added as admin to the DB channel and
  all 4 force-sub channels, or that bot will fail its startup check and exit.
- Posting a new file to the shared DB channel will trigger all running bots
  to react to it (since they all watch the same channel) — this is expected
  and harmless; each bot just generates/edits the file-share button on the
  channel post.
- Admin commands (`/broadcast`, `/pin`, `/unpin`, `/users`) are scoped to
  whichever bot you message — each bot only touches its own subscriber list.
