from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from config import *

from keyboards.admin import *

from FSM.allFSMs import *

from database.flash_admin import *
from database.users import get_user, save_user, update_user_photo, get_all_users, get_user_by_photo, delete_user
from database.points import *

from database.db import db

users_collection = db["users"]
points_collection = db["points"]

async def get_total_users():
    return await users_collection.count_documents({})

async def get_total_points():
    return await points_collection.count_documents({})

async def get_total_photos():
    return await users_collection.count_documents({"photo": {"$ne": None}})

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in MAIN_ADMINS:
        await message.answer("❌ У вас немає доступу до цієї команди.")
        return

    await message.answer(
        "👮‍♂️ <b>Адмін-панель</b>\n\n"
        "Оберіть одну з доступних опцій:",
        reply_markup=get_admin_panel_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "cancel_action")
async def back_to_admin_panel(callback: CallbackQuery):
    if callback.from_user.id not in MAIN_ADMINS:
        await callback.message.edit_text("❌ У вас немає доступу до цієї команди.")
        return

    await callback.message.edit_text(
        "👮‍♂️ <b>Адмін-панель</b>\n\n"
        "Оберіть одну з доступних опцій:",
        reply_markup=get_admin_panel_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "flash_admins")
async def flash_admins_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        "📸 <b>Флеш-адміни</b>\n\n"
        "Оберіть одну з доступних опцій:",
        reply_markup=get_flash_admins_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "exit_admin_panel")
async def exit_admin_panel(callback: CallbackQuery):
    await callback.message.edit_text("👋 Ви вийшли з адмін-панелі.")

@router.callback_query(F.data == "add_flash_admin")
async def add_flash_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "✏️ Введіть ID користувача, якого ви хочете зробити флеш-адміном:",
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_flash_admin_id)

@router.message(F.text, AdminStates.waiting_for_flash_admin_id)
async def process_flash_admin_id(message: Message, state: FSMContext):
    try:
        admin_id = int(message.text)
        await create_flash_admin(admin_id)
        await message.answer(
            f"✅ Користувача з ID <b>{admin_id}</b> успішно додано як флеш-адміна!",
            parse_mode="HTML",
            reply_markup=get_flash_admins_keyboard()
        )
    except ValueError:
        await message.answer("❌ Будь ласка, введіть коректний числовий ID.")
    finally:
        await state.clear()

@router.callback_query(F.data == "shuffle_photos")
async def shuffle_photos_handler(callback: CallbackQuery):
    await callback.message.edit_text("🔄 Починаємо перемішування списків фото для всіх флеш-адмінів...")

    await shuffle_photos_for_all_admins()

    await callback.message.edit_text(
        "✅ Списки фото успішно перемішані для всіх флеш-адмінів!",
        reply_markup=get_flash_admins_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "special_functions")
async def special_functions_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        "🛠 <b>Спеціальні функції</b>\n\n"
        "Оберіть одну з доступних опцій:",
        reply_markup=get_special_functions_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "broadcast_message")
async def broadcast_message_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📢 Введіть текст повідомлення, яке потрібно розіслати всім користувачам:",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_broadcast_message)


@router.message(AdminStates.waiting_for_broadcast_message)
async def process_broadcast_message(message: Message, state: FSMContext):
    broadcast_text = message.text

    users = await get_all_users()

    user_count = len(users)
    user_list_preview = "\n".join(
        [f"👤 {user.get('full_name', 'Невідомий')} (ID: {user['user_id']})" for user in users[:10]]
    )
    if len(users) > 10:
        user_list_preview += f"\n...та ще {len(users) - 10} користувачів."

    await message.answer(
        f"📢 <b>Попередній перегляд розсилки:</b>\n\n"
        f"✉️ <b>Текст повідомлення:</b>\n{broadcast_text}\n\n"
        f"👥 <b>Кількість отримувачів:</b> {user_count}\n\n"
        f"📝 <b>Список отримувачів:</b>\n{user_list_preview}",
        parse_mode="HTML",
        reply_markup=get_confirm_broadcast_keyboard()
    )
    await state.update_data(broadcast_text=broadcast_text, users=users)
    await state.set_state(AdminStates.waiting_for_broadcast_confirmation)

@router.callback_query(F.data == "confirm_broadcast")
async def confirm_broadcast(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    broadcast_text = data.get("broadcast_text")
    users = data.get("users")

    for user in users:
        try:
            await callback.bot.send_message(chat_id=user["user_id"], text=broadcast_text)
        except Exception as e:
            print(f"Не вдалося відправити повідомлення користувачу {user['user_id']}: {e}")

    await callback.message.edit_text("✅ Повідомлення успішно розіслано всім користувачам!")
    await state.clear()

@router.callback_query(F.data == "check_creative_photo")
async def check_creative_photo(callback: CallbackQuery):
    admins = await get_all_flash_admins()

    photo_scores = {}
    for admin in admins:
        ratings = admin.get("photo_ratings", {})
        for photo_id, score in ratings.items():
            if photo_id not in photo_scores:
                photo_scores[photo_id] = 0
            photo_scores[photo_id] += score

    if not photo_scores:
        await callback.message.edit_text("❌ Немає оцінених фото.")
        return

    best_photo_id = max(photo_scores, key=photo_scores.get)
    best_score = photo_scores[best_photo_id]

    user = await get_user_by_photo(best_photo_id)
    if user:
        user_name = user.get("full_name", "Невідомий користувач")
        user_id = user.get("user_id", "Невідомий ID")
    else:
        user_name = "Невідомий користувач"
        user_id = "Невідомий ID"

    users = await get_all_users()
    for user in users:
        try:
            await callback.bot.send_photo(
                chat_id=user["user_id"],
                photo=best_photo_id,
                caption=(
                    f"🏆 <b>Найкреативніше фото з Райаном Гослінгом!</b>\n\n"
                    f"📸 <b>Автор:</b> {user_name} (ID: {user_id})\n"
                    f"⭐ <b>Кількість балів:</b> {best_score}\n\n"
                    f"Дякуємо всім за участь! ❤️\n\n"
                    f"📩 <b>З переможцем скоро зв'яжуться для вручення нагороди!</b>"
                ),
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Не вдалося відправити повідомлення користувачу {user['user_id']}: {e}")

    await callback.message.edit_text(
        f"✅ Результати розіслані! Фото-переможець: {best_photo_id} з {best_score} балами.\n"
        f"📸 Автор: {user_name} (ID: {user_id})\n\n"
        f"📩 <b>З переможцем скоро зв'яжуться для вручення нагороди!</b>",
        reply_markup=get_special_functions_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "users")
async def users_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        "👥 <b>Користувачі</b>\n\n"
        "Оберіть одну з доступних опцій:",
        reply_markup=get_users_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "edit_user")
async def edit_user_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "✏️ Введіть ID користувача, якого ви хочете змінити:",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_user_edit_id)


@router.message(AdminStates.waiting_for_user_edit_id)
async def process_user_edit_id(message: Message, state: FSMContext):
    user_id = int(message.text)
    user = await get_user(user_id)

    if not user:
        await message.answer("❌ Користувача з таким ID не знайдено.")
        await state.clear()
        return

    await state.update_data(user_id=user_id)
    await message.answer(
        f"✅ Користувача знайдено: <b>{user.get('full_name', 'Невідомий')}</b>\n\n"
        "Введіть нові дані у форматі:\n"
        "<code>Ім'я, Номер телефону, Попередня школа</code>",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(AdminStates.waiting_for_user_edit_data)


@router.message(AdminStates.waiting_for_user_edit_data)
async def process_user_edit_data(message: Message, state: FSMContext):
    data = message.text.split(",")
    if len(data) != 3:
        await message.answer("❌ Невірний формат. Введіть дані у форматі:\n<code>Ім'я, Номер телефону, Попередня школа</code>", parse_mode="HTML")
        return

    user_data = {
        "full_name": data[0].strip(),
        "phone_number": data[1].strip(),
        "previous_school": data[2].strip()
    }

    state_data = await state.get_data()
    user_id = state_data["user_id"]

    await users_collection.update_one({"user_id": user_id}, {"$set": user_data})
    await message.answer("✅ Дані користувача успішно оновлено!")
    await state.clear()

@router.callback_query(F.data == "delete_user_photo")
async def delete_user_photo_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "✏️ Введіть ID користувача, у якого потрібно видалити фото:",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_user_photo_delete_id)


@router.message(AdminStates.waiting_for_user_photo_delete_id)
async def process_user_photo_delete_id(message: Message, state: FSMContext):
    user_id = int(message.text)
    user = await get_user(user_id)

    if not user or not user.get("photo"):
        await message.answer("❌ Користувача з таким ID або фото не знайдено.")
        await state.clear()
        return

    await update_user_photo(user_id, None)
    await message.answer("✅ Фото користувача успішно видалено!")
    await state.clear()

@router.callback_query(F.data == "delete_user")
async def delete_user_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "✏️ Введіть ID користувача, якого потрібно видалити:",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_user_delete_id)


@router.message(AdminStates.waiting_for_user_delete_id)
async def process_user_delete_id(message: Message, state: FSMContext):
    user_id = int(message.text)
    user = await get_user(user_id)

    if not user:
        await message.answer("❌ Користувача з таким ID не знайдено.")
        await state.clear()
        return

    await delete_user(user_id)
    await message.answer("✅ Користувача успішно видалено!")
    await state.clear()

@router.callback_query(F.data == "view_ratings")
async def view_ratings(callback: CallbackQuery):
    admins = await get_all_flash_admins()

    if not admins:
        await callback.message.edit_text("❌ Немає доступних оцінок.")
        return

    ratings_summary = "📊 <b>Оцінки фото:</b>\n\n"

    for admin in admins:
        admin_id = admin.get("admin_id", "Невідомий ID")
        admin_user = await get_user(admin_id)
        admin_name = admin_user.get("full_name", "Невідомий адмін") if admin_user else f"ID: {admin_id}"

        photo_ratings = admin.get("photo_ratings", {})

        if not photo_ratings:
            ratings_summary += f"👮‍♂️ <b>Адмін {admin_name}:</b> Немає оцінок.\n"
            continue

        ratings_summary += f"👮‍♂️ <b>Адмін {admin_name}:</b>\n"
        for photo_id, score in photo_ratings.items():
            user = await get_user_by_photo(photo_id)
            if user:
                user_name = user.get("full_name", "Невідомий користувач")
                user_id = user.get("user_id", "Невідомий ID")
                ratings_summary += f"📸 <b>Автор:</b> {user_name} (ID: {user_id}) — ⭐ {score} балів\n"
            else:
                ratings_summary += f"📸 <b>Автор:</b> Невідомий користувач — ⭐ {score} балів\n"
        ratings_summary += "\n"

    await callback.message.edit_text(
        ratings_summary,
        parse_mode="HTML",
        reply_markup=get_flash_admins_keyboard()
    )

@router.callback_query(F.data == "points")
async def points_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        "📍 <b>Точки</b>\n\n"
        "Оберіть одну з доступних опцій:",
        reply_markup=get_points_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "add_point")
async def add_point_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "✏️ Введіть назву точки:",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_point_name)


@router.message(AdminStates.waiting_for_point_name)
async def process_point_name(message: Message, state: FSMContext):
    point_name = message.text.strip()
    await state.update_data(point_name=point_name)

    await message.answer(
        "✏️ Тепер введіть опис точки:",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_point_description)

@router.message(AdminStates.waiting_for_point_description)
async def process_point_description(message: Message, state: FSMContext):
    point_description = message.text.strip()
    state_data = await state.get_data()
    point_name = state_data.get("point_name")

    point = await add_point(name=point_name, description=point_description)

    await message.answer(
        f"✅ Точку успішно додано:\n\n"
        f"📍 <b>Назва:</b> {point['name']}\n"
        f"📝 <b>Опис:</b> {point['description']}\n"
        f"🔑 <b>Код:</b> {point['code']}",
        parse_mode="HTML"
    )
    await state.clear()

@router.callback_query(F.data == "view_points")
async def view_points(callback: CallbackQuery):
    points = await get_all_points()

    if not points:
        await callback.message.edit_text("❌ Немає доступних точок.")
        return

    points_summary = "📋 <b>Список точок:</b>\n\n"
    for point in points:
        points_summary += (
            f"📍 <b>Назва:</b> {point['name']}\n"
            f"📝 <b>Опис:</b> {point['description']}\n"
            f"🔑 <b>Код:</b> {point['code']}\n\n"
        )

    await callback.message.edit_text(
        points_summary,
        parse_mode="HTML",
        reply_markup=get_points_keyboard()
    )

@router.callback_query(F.data == "edit_point")
async def edit_point_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "✏️ Введіть код точки, яку ви хочете змінити:",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_point_code)


@router.message(AdminStates.waiting_for_point_code)
async def process_edit_point_code(message: Message, state: FSMContext):
    code = int(message.text)
    point = await get_point_by_code(code)

    if not point:
        await message.answer("❌ Точку з таким кодом не знайдено.")
        await state.clear()
        return

    await state.update_data(point_code=code)
    await message.answer(
        f"✅ Точку знайдено:\n\n"
        f"📍 <b>Назва:</b> {point['name']}\n"
        f"📝 <b>Опис:</b> {point['description']}\n\n"
        "✏️ Введіть нову назву точки:",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_point_new_name)

@router.message(AdminStates.waiting_for_point_new_name)
async def process_edit_point_name(message: Message, state: FSMContext):
    new_name = message.text.strip()
    await state.update_data(new_name=new_name)

    await message.answer(
        "✏️ Тепер введіть новий опис точки:",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_point_new_description)   

@router.message(AdminStates.waiting_for_point_new_description)
async def process_edit_point_description(message: Message, state: FSMContext):
    new_description = message.text.strip()
    state_data = await state.get_data()
    code = state_data.get("point_code")
    new_name = state_data.get("new_name")

    updated = await update_point(code=code, name=new_name, description=new_description)
    if updated:
        await message.answer("✅ Точку успішно оновлено!")
    else:
        await message.answer("❌ Не вдалося оновити точку.")
    await state.clear()

@router.callback_query(F.data == "delete_point")
async def delete_point_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "✏️ Введіть код точки, яку ви хочете видалити:",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_for_point_delete)


@router.message(AdminStates.waiting_for_point_delete)
async def process_delete_point(message: Message, state: FSMContext):
    code = int(message.text)
    deleted = await delete_point(code)

    if deleted:
        await message.answer("✅ Точку успішно видалено!")
    else:
        await message.answer("❌ Точку з таким кодом не знайдено.")
    await state.clear()


@router.callback_query(F.data == "statistics")
async def statistics_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        "📊 <b>Статистика</b>\n\n"
        "Оберіть одну з доступних опцій:",
        reply_markup=get_statistics_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "general_statistics")
async def general_statistics(callback: CallbackQuery):



    total_users = await get_total_users()
    total_points = await get_total_points()
    total_photos = await get_total_photos()

    await callback.message.edit_text(
        f"📊 <b>Загальна статистика:</b>\n\n"
        f"👥 <b>Кількість користувачів:</b> {total_users}\n"
        f"📍 <b>Кількість точок:</b> {total_points}\n"
        f"📸 <b>Кількість фото:</b> {total_photos}\n",
        parse_mode="HTML",
        reply_markup=get_statistics_keyboard()
    )


@router.callback_query(F.data == "list_users")
async def list_users(callback: CallbackQuery):
    users = await get_all_users()

    if not users:
        await callback.message.edit_text("❌ Немає зареєстрованих користувачів.")
        return

    users_summary = "👥 <b>Список користувачів:</b>\n\n"
    for user in users[:50]:
        users_summary += f"👤 <b>{user.get('full_name', 'Невідомий')}</b> (ID: {user['user_id']})\n"

    if len(users) > 50:
        users_summary += f"\n...та ще {len(users) - 50} користувачів."

    await callback.message.edit_text(
        users_summary,
        parse_mode="HTML",
        reply_markup=get_statistics_keyboard()
    )

@router.callback_query(F.data == "photo_statistics")
async def photo_statistics(callback: CallbackQuery):
    total_photos = await get_total_photos()

    await callback.message.edit_text(
        f"📸 <b>Статистика фото:</b>\n\n"
        f"📸 <b>Кількість завантажених фото:</b> {total_photos}\n",
        parse_mode="HTML",
        reply_markup=get_statistics_keyboard()
    )

@router.callback_query(F.data == "ratings_statistics")
async def ratings_statistics(callback: CallbackQuery):
    admins = await get_all_flash_admins()

    if not admins:
        await callback.message.edit_text("❌ Немає доступних оцінок.")
        return

    ratings_summary = "⭐ <b>Статистика оцінок:</b>\n\n"
    for admin in admins:
        admin_id = admin.get("admin_id", "Невідомий ID")
        photo_ratings = admin.get("photo_ratings", {})

        ratings_summary += f"👮‍♂️ <b>Адмін {admin_id}:</b> {len(photo_ratings)} оцінок\n"

    await callback.message.edit_text(
        ratings_summary,
        parse_mode="HTML",
        reply_markup=get_statistics_keyboard()
    )

@router.callback_query(F.data == "points_statistics")
async def points_statistics(callback: CallbackQuery):
    points = await get_all_points()

    if not points:
        await callback.message.edit_text("❌ Немає доступних точок.")
        return

    points_summary = "📍 <b>Статистика точок:</b>\n\n"
    points_summary += f"📍 <b>Кількість точок:</b> {len(points)}\n"

    await callback.message.edit_text(
        points_summary,
        parse_mode="HTML",
        reply_markup=get_statistics_keyboard()
    )

@router.callback_query(F.data == "run_raffle")
async def run_raffle(callback: CallbackQuery):
    users = await users_collection.find({"is_complited": True}).to_list(length=None)

    if not users:
        await callback.message.edit_text("❌ Немає учасників для розіграшу.")
        return

    winner = random.choice(users)
    winner_name = winner.get("full_name", "Невідомий користувач")
    winner_id = winner.get("user_id", "Невідомий ID")

    try:
        await callback.bot.send_message(
            chat_id=winner_id,
            text=(
                f"🎉 <b>Вітаємо, {winner_name}!</b>\n\n"
                f"🏆 Ви стали переможцем розіграшу!\n\n"
                f"📩 З вами скоро зв'яжуться для вручення нагороди.\n\n"
                f"❤️ Дякуємо за участь!"
            ),
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Не вдалося відправити повідомлення переможцю {winner_id}: {e}")

    await callback.message.edit_text(
        f"🎉 <b>Розіграш завершено!</b>\n\n"
        f"🏆 <b>Переможець:</b> {winner_name} (ID: {winner_id})\n\n"
        f"📩 <b>З переможцем скоро зв'яжуться для вручення нагороди!</b>",
        parse_mode="HTML",
        reply_markup=get_special_functions_keyboard()
    )