import os
import asyncio
import logging
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import async_main
from dotenv import load_dotenv

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
#bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher()
async def main():
    await async_main()
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")    
        