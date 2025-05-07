import asyncio
import logging

from aiogram import Bot, Dispatcher
import asyncio
from config import TOKEN
from handlers.reg import router as reg_router
from handlers.photo import router as photo_router
from handlers.quest import router as quest_router
from handlers.admin.admin_panel import router as admin_router
from handlers.grade import router as grade_router
from database.db import test_connection


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    await test_connection()

    dp.include_router(reg_router)
    dp.include_router(quest_router)
    dp.include_router(photo_router)
    dp.include_router(admin_router)
    dp.include_router(grade_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())