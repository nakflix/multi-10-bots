import asyncio

from dotenv import load_dotenv
load_dotenv()

from config import BOTS, LOGGER
from levi import Bot

log = LOGGER(__name__)


async def main():
    bots = []
    for cfg in BOTS:
        bot = Bot(
            bot_name=cfg["name"],
            bot_token=cfg["token"],
            db_uri=cfg["db_uri"],
            db_name=cfg["db_name"],
            port=cfg["port"],
        )
        bots.append(bot)

    log.info(f"Starting {len(bots)} bot(s)...")

    # Start all bots concurrently
    await asyncio.gather(*(bot.start() for bot in bots))

    log.info("All bots started. Running...")

    # Keep the process alive forever
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
