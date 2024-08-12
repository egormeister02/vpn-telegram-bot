import asyncio
import asyncpg

from aiogram import types, F, Router
from aiogram.filters import Command
import logging

router = Router()

# Здесь хранятся пользовательские данные. Для продакшн-версии рекомендуется использовать базу данных.
user_data = {}

menu_buttons = [
    [
        types.InlineKeyboardButton(text="Подключить", callback_data="menu_connect"),
        types.InlineKeyboardButton(text="Личный кабинет", callback_data="menu_user")
    ],
    [
        types.InlineKeyboardButton(text="Пополнить счет", callback_data="menu_up_balance"),
        types.InlineKeyboardButton(text="О проекте", callback_data="menu_about")
    ]
]
menu_keyboard = types.InlineKeyboardMarkup(inline_keyboard=menu_buttons)


@router.message(Command("start"))
async def cmd_start(message: types.Message, pool: asyncpg.pool.Pool):
    try:
        async with pool.acquire() as conn:
            user_id = message.from_user.id
            user_name = message.from_user.username or "Unknown"
            
            # Проверяем, существует ли пользователь в базе данных
            row = await conn.fetchrow("SELECT balance_rub FROM main.users WHERE user_id=$1", user_id)
            
            if row:
                balance = row['balance_rub']
                await message.answer(f"Добро пожаловать, {user_name}!\nВаш баланс: {balance} руб.", reply_markup=menu_keyboard)
            else:
                # Если пользователя нет в базе, добавляем его с начальным балансом 0
                await conn.execute("""
                    INSERT INTO main.users (user_id, user_nm, balance_rub) VALUES ($1, $2, $3)
                    """, user_id, user_name, 0)
                
                # После добавления нового пользователя, отобразим его баланс
                await message.answer(f"Добро пожаловать, {user_name}!\nВаш баланс: 0 руб.", reply_markup=menu_keyboard)
    except asyncpg.PostgresError as e:
        logging.error(f"Database error: {e}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        await message.answer("Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже.")

@router.callback_query(F.data.startswith("menu_"))
async def callbacks_menu(callback: types.CallbackQuery, pool: asyncpg.pool.Pool):
    try:
        async with pool.acquire() as conn:
            user_id = callback.from_user.id
            action = callback.data.split("_")[1]

            if action == "connect":
                await callback.message.answer("Вы подключились")
            elif action == "user":
                row = await conn.fetchrow("SELECT balance_rub FROM main.users WHERE user_id=$1", user_id)
                if row:
                    balance = row['balance_rub']
                    await callback.message.answer(f"Ваш баланс: {balance} руб.")
                else:
                    await callback.message.answer("Информация о вас не найдена.")
            elif action == "up":
                await callback.message.answer("Введите сумму")
            elif action == "about":
                await callback.message.answer("О проекте")
            else:
                await callback.message.answer("Неизвестное действие")
                
    except asyncpg.PostgresError as e:
        logging.error(f"Database error: {e}")
        await callback.message.answer("Произошла ошибка при взаимодействии с базой данных. Пожалуйста, попробуйте позже.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        await callback.message.answer("Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже.")

    await callback.answer()
