from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter


from config import *

from FSM.allFSMs import *

from database.users import get_user, save_user, update_user_photo

from keyboards.reg import *
from keyboards.photo import *

router = Router()

@router.callback_query(F.data == "make_photo")
async def request_photo(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if user["photo"]:
        await callback.message.edit_text(
            "❌ Ви вже надіслали фото раніше. Ви можете зробити це лише один раз!"
        )
        return
    else:
        await callback.message.edit_text(
            "📸 Надішліть, будь ласка, ваше фото. Ви можете зробити це лише один раз!"
        )
        await state.set_state(PhotoStates.waiting_for_photo)


@router.message(StateFilter(PhotoStates.waiting_for_photo), F.photo)
async def save_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id

    await update_user_photo(user_id=message.from_user.id, photo_id=photo_id)

    await message.delete()
    await message.answer("✅ Ваше фото успішно збережено! Дякуємо за участь.", reply_markup=get_main_menu_keyboard())

    await state.clear()