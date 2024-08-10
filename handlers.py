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
async def cmd_start(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Добро пожаловать", reply_markup=menu_keyboard)

@router.callback_query(F.data.startswith("menu_"))
async def callbacks_menu(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    global db_pool  # Доступ к глобальной переменной

    if action == "connect":
        await callback.message.answer("Вы подключились")
    elif action == "user":
        await callback.message.answer(f"Ваш id: {callback.from_user.id}")
    elif action == "up":
        await callback.message.answer("Введите сумму")
    elif action == "about":
        await callback.message.answer("О проекте")
    else:
        await callback.message.answer("Неизвестное действие")

    await callback.answer()

