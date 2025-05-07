from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_panel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👮‍♂️ Флеш-адміни", callback_data="flash_admins"),
            InlineKeyboardButton(text="📍 Точки", callback_data="points")
        ],
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="statistics"),
            InlineKeyboardButton(text="✨ Спец функції", callback_data="special_functions")
        ],
        [
            InlineKeyboardButton(text="👥 Користувачі", callback_data="users"),
            InlineKeyboardButton(text="🚪 Вийти", callback_data="exit_admin_panel")
        ]
    ])

def get_flash_admins_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Додати флеш-адміна", callback_data="add_flash_admin"),
            InlineKeyboardButton(text="🔄 Перемішати фото", callback_data="shuffle_photos")
        ],
        [
            InlineKeyboardButton(text="📋 Переглянути оцінки", callback_data="view_ratings")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад до адмін-панелі", callback_data="cancel_action")
        ]
    ])

def get_flash_admins_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Додати флеш-адміна", callback_data="add_flash_admin"),
            InlineKeyboardButton(text="🔄 Перемішати фото", callback_data="shuffle_photos")
        ],
        [
            InlineKeyboardButton(text="📋 Переглянути оцінки", callback_data="view_ratings")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад до адмін-панелі", callback_data="cancel_action")
        ]
    ])

def get_cancel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel_action")]
    ])

def get_special_functions_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📢 Розсилка всім", callback_data="broadcast_message"),
            InlineKeyboardButton(text="🏆 Перевірка переможця", callback_data="check_creative_photo")
        ],
        [
            InlineKeyboardButton(text="🎉 Розіграш серед учасників", callback_data="run_raffle")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="cancel_action")
        ]
    ])

def get_users_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Змінити користувача", callback_data="edit_user"),
            InlineKeyboardButton(text="🖼 Видалити фото", callback_data="delete_user_photo")
        ],
        [
            InlineKeyboardButton(text="❌ Видалити користувача", callback_data="delete_user")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="cancel_action")
        ]
    ])

def get_confirm_broadcast_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Підтвердити", callback_data="confirm_broadcast"),
            InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel_action")
        ]
    ])

def get_points_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Додати точку", callback_data="add_point"),
            InlineKeyboardButton(text="✏️ Змінити точку", callback_data="edit_point")
        ],
        [
            InlineKeyboardButton(text="🗑 Видалити точку", callback_data="delete_point"),
            InlineKeyboardButton(text="📋 Переглянути точки", callback_data="view_points")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад до адмін-панелі", callback_data="cancel_action")
        ]
    ])

def get_statistics_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👥 Список користувачів", callback_data="list_users"),
            InlineKeyboardButton(text="📸 Статистика фото", callback_data="photo_statistics")
        ],
        [
            InlineKeyboardButton(text="⭐ Статистика оцінок", callback_data="ratings_statistics"),
            InlineKeyboardButton(text="📍 Статистика точок", callback_data="points_statistics")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад до адмін-панелі", callback_data="cancel_action")
        ]
    ])