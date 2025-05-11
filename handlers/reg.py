from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import *

from FSM.allFSMs import *

from database.users import get_user, save_user
from database.db import db

from keyboards.reg import *

router = Router()

@router.message(CommandStart())
async def send_welcome(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if user:
      await message.answer(
          f"👋 Вітаємо назад, {user['full_name']}! 🎓\n\n"
          "Ви вже зареєстровані на екскурсію по 3 корпусу ДНУ — "
          "Факультету прикладної математики та інформаційних технологій. 🏫\n\n"
          f"📞 Ваш номер телефону: {user['phone_number']}\n"
          f"🏫 Ваш попередній навчальний заклад: {user['previous_school']}\n\n"
          "📍 Ми з нетерпінням чекаємо на вашу участь у нашій екскурсії!",
          reply_markup=main_keyboard
      )
      return

    await message.answer(
        "👋 Вітаємо! Ви записуєтесь на екскурсію по 3 корпусу ДНУ — "
        "Факультету прикладної математики та інформаційних технологій. 🎓\n\n"
        "Для початку, будь ласка, зареєструйтесь.\n"
        "📋 Введіть своє повне ім'я (ПІБ):"
    )
    await state.set_state(Registration.full_name)

@router.message(Registration.full_name, F.text)
async def ask_phone_number(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text) 

    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Надіслати номер телефону", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "✅ Дякуємо! Тепер надішліть свій номер телефону, натиснувши кнопку нижче:",
        reply_markup=contact_keyboard
    )
    await state.set_state(Registration.phone_number)


@router.message(Registration.phone_number, F.contact)
async def ask_previous_school(message: Message, state: FSMContext):
    contact = message.contact
    await state.update_data(phone_number=contact.phone_number)

    await message.answer(
        "🏫 Дякуємо! Тепер вкажіть, будь ласка, назву вашого поточного навчального закладу:"
    )
    await state.set_state(Registration.previous_school)


@router.message(Registration.previous_school, F.text)
async def finish_registration(message: Message, state: FSMContext):
    await state.update_data(previous_school=message.text)

    user_data = await state.get_data()

    await save_user(
        user_id=message.from_user.id,
        full_name=user_data['full_name'],
        phone_number=user_data['phone_number'],
        previous_school=user_data['previous_school']
    )

    await message.answer(
        f"✅ Реєстрація завершена!\n\n"
        f"Ваші дані:\n"
        f"👤 ПІБ: {user_data['full_name']}\n"
        f"📞 Телефон: {user_data['phone_number']}\n"
        f"🏫 Попередній навчальний заклад: {user_data['previous_school']}\n\n"
        "Дякуємо за реєстрацію! Ви можете почати користуватися нашим сервісом.",
        reply_markup=main_keyboard
    )

    await state.clear()

@router.callback_query(F.data == "main_menu")
@router.callback_query(F.data == "cancel_action")
async def send_activities_description(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "🎉 <b>Наші активності під час екскурсії:</b>\n\n"
        "1️⃣ <b>Зробити найкреативніше фото з Райаном Гослінгом</b> 📸\n"
        "<i>Покажіть свою креативність та отримайте шанс виграти приз!</i>\n\n"
        "2️⃣ <b>Відсканувати всі QR-коди під час екскурсії</b> 📷\n"
        "<i>Збирайте QR-коди, щоб прийняти участь у розіграші цікавих подарунків!</i>\n\n"
        "<b>Оберіть дію, щоб розпочати:</b>",
        reply_markup=get_registration_keyboard,
        parse_mode="HTML"
    )