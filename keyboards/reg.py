from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

get_registration_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📸 Зробити фото", callback_data="make_photo"),
            InlineKeyboardButton(text="📷 Відсканувати QR", callback_data="scan_qr")
        ]
    ])

main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🏠 Головне меню", callback_data="main_menu")
        ]
    ])