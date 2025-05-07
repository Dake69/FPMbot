from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import *

from FSM.allFSMs import *

from database.users import users_collection

from database.points import get_all_points

router = Router()

@router.callback_query(lambda c: c.data == "enter_qr")
async def ask_for_qr(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(QRCode.take_qrcode)
    await callback_query.message.answer("Відправте QR код.")

@router.message(QRCode.take_qrcode, F.text)
async def receive_qr(message: types.Message, state: FSMContext):
    qr_code = int(message.text.strip())
    points_array = await get_all_points()
    point_found = False


    for point in points_array:
        if (point['code'] == qr_code):
            users_collection.update_one(
            {"user_id": message.chat.id},
            {"$push": {"point_complited": qr_code}})
            await message.answer("Ваш код було прийнято!")
            point_found = True
 
    if point_found == False:
        await message.answer("Код не було знайдено.")
    
    await state.clear()

    
