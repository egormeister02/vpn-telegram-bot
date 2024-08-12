import asyncio
import asyncpg
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers import router

async def create_db_pool():
    try:
        pool = await asyncpg.create_pool(
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            database=config.POSTGRES_DB,
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT
        )
        logging.info("Successfully connected to the database!")
        return pool
    except Exception as e:
        logging.error(f"Error creating a connection pool with the database: {e}")
        raise

async def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting the application...")

    pool = await create_db_pool()

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    dp["pool"] = pool

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), parse_mode=ParseMode.HTML)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
