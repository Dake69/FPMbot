from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

import random

router = Router()

from config import *

from FSM.allFSMs import *

from database.flash_admin import *
from database.users import get_all_photos

from keyboards.grade import get_grade_keyboard

@router.message(Command("grade"))
async def flash_admin_menu(message: Message, state: FSMContext):
    all_admins = await get_all_flash_admins()

    if not any(admin["admin_id"] == message.from_user.id for admin in all_admins) and message.from_user.id not in MAIN_ADMINS:
        await message.answer("❌ У вас немає доступу до цієї команди.")
        return

    all_photos = await get_all_photos()

    random.shuffle(all_photos)

    if not all_photos:
        await message.answer("❌ У вас немає фото для оцінювання.")
        return

    if isinstance(all_photos[0], dict) and "photo" in all_photos[0]:
        photo_id = all_photos[0]["photo"]
    else:
        await message.answer("❌ Некоректна структура даних для фото.")
        return

    await state.update_data(photos=all_photos)

    await message.answer_photo(
        photo=photo_id,
        caption="📸 Оцініть це фото:",
        reply_markup=get_grade_keyboard(photo_id)
    )


@router.callback_query(F.data.startswith("g"))
async def process_grade(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    if len(parts) != 3:
        await callback.answer("❌ Некоректні дані кнопки.", show_alert=True)
        return

    _, grade, photo_id = parts
    grade = int(grade)

    data = await state.get_data()
    photos = data.get("photos", [])
    if photos:
        current_photo = photos.pop(0)
        await state.update_data(photos=photos)

        original_photo_id = current_photo["photo"]

        await rate_photo(callback.from_user.id, original_photo_id, grade)

    await callback.message.edit_caption("✅ Оцінка збережена!")

    if photos:
        next_photo_id = photos[0]["photo"]
        await callback.message.answer_photo(
            photo=next_photo_id,
            caption="📸 Оцініть наступне фото:",
            reply_markup=get_grade_keyboard(next_photo_id)
        )
    else:
        await callback.message.answer("✅ Ви оцінили всі доступні фото!")
        await state.clear()