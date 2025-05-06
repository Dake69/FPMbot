from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    full_name = State()
    phone_number = State()
    previous_school = State()


class QRCode(StatesGroup):
    take_qrcode = State()