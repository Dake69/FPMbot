import hashlib
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_grade_keyboard(photo_id: str):
    if not isinstance(photo_id, str):
        photo_id = str(photo_id)

    hashed_photo_id = hashlib.md5(photo_id.encode()).hexdigest()[:10]
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1️⃣", callback_data=f"g_1_{hashed_photo_id}"),
            InlineKeyboardButton(text="2️⃣", callback_data=f"g_2_{hashed_photo_id}"),
            InlineKeyboardButton(text="3️⃣", callback_data=f"g_3_{hashed_photo_id}"),
            InlineKeyboardButton(text="4️⃣", callback_data=f"g_4_{hashed_photo_id}"),
            InlineKeyboardButton(text="5️⃣", callback_data=f"g_5_{hashed_photo_id}")
        ]
    ])