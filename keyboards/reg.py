from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

get_registration_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📸 Зробити фото", callback_data="make_photo"),
            InlineKeyboardButton(text="📷 Ввести код локації", callback_data="enter_qr")
        ]
    ])

main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🏠 Головне меню", callback_data="main_menu")
        ]
    ])