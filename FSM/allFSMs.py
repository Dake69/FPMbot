from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    full_name = State()
    phone_number = State()
    previous_school = State()


class QRCode(StatesGroup):
    take_qrcode = State()

class PhotoStates(StatesGroup):
    waiting_for_photo = State()

class AdminStates(StatesGroup):
    waiting_for_flash_admin_id = State()
    waiting_for_broadcast_message = State()
    waiting_for_user_edit_id = State()
    waiting_for_user_edit_data = State()
    waiting_for_user_photo_delete_id = State()
    waiting_for_user_delete_id = State()
    waiting_for_point_name = State()
    waiting_for_point_description = State()
    waiting_for_point_code = State()
    waiting_for_point_new_name = State()
    waiting_for_point_new_description = State()
    waiting_for_point_delete = State()