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
        return await asyncpg.create_pool(
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            database=config.POSTGRES_DB,
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT
        )
    except Exception as e:
        logging.error(f"Ошибка при создании пула соединений с базой данных: {e}")
        raise

async def main():
    logging.info("Запуск приложения...")
    
    pool = await create_db_pool()

    # Здесь добавьте лог перед тем, как будет выполнен запрос к базе данных
    logging.info("Подключение к базе данных и получение данных...")

    await fetch_accounts(pool)

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), parse_mode=ParseMode.HTML)


async def fetch_accounts(pool):
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM main.users")
        for row in rows:
            logging.info(f"Получены данные из базы: {row}")
    await pool.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
