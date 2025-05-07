from aiogram import F, Router, types, Bot
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from pyzbar.pyzbar import decode
from config import TOKEN
from PIL import Image
import io
import requests

from config import *

from FSM.allFSMs import *

from database.users import users_collection, get_user, get_user_by_id_and_point, get_point_complited_count

from database.points import get_point_by_code, get_all_points, points_collection

router = Router()
bot = Bot(token=TOKEN)

@router.callback_query(lambda c: c.data == "enter_qr")
async def ask_for_qr(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(QRCode.take_qrcode)
    await callback_query.message.answer("Відправте фото QR коду.")

@router.message(QRCode.take_qrcode, F.photo)
async def receive_qr(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path


    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"  
    response = requests.get(file_url)
    
    image = Image.open(io.BytesIO(response.content))
    decoded_data = decode(image)

    if not decoded_data:
        await message.answer("Не вдалося розпізнати QR-код. Будь ласка, спробуйте ще раз.")
        return
    
    qr_code = int(decoded_data[0].data.decode("utf-8"))

    user_col = await get_user_by_id_and_point(message.chat.id, qr_code)

    if user_col and "point_complited" in user_col:
        if qr_code in user_col["point_complited"]:
            await message.answer("Ви вже ввели цей код.")
            return

 
    point_passed = await get_point_by_code(qr_code)

    if point_passed is not None:
        users_collection.update_one(
            {"user_id": message.chat.id},
            {"$addToSet": {"point_complited": qr_code}}  
        )
        await message.answer("Вітаємо з проходженням точки " + point_passed['name'] + "!\nОпис точки: " + point_passed['description'])

    completed_points = await users_collection.count_documents({"user_id": message.chat.id})
    all_points = await points_collection.count_documents({}) 

    print(completed_points)
    print(all_points)

    if completed_points == all_points:
        users_collection.update_one(
            {"user_id": message.chat.id},
            {"$set": {"is_complited": True}}
        )
        await message.answer("Вітаю! Ви успішно пройшли всі точки, долаючи кожен етап із впевненістю та наполегливістю. Тепер ви маєте можливість прийняти участь в розіграші!🎉")

    await state.clear()