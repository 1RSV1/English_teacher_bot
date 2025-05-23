import os
import asyncio
import logging
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from app.database.requests import retrieve_inactive_users
from app.handlers import router, find_time, bot
from app.database.models import async_main
from dotenv import load_dotenv
import datetime

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
#bot = Bot(token=os.getenv('TOKEN'))
async def scheduler(delay: int):
    #chat_ids = [155269575]  # ids
    while True:
        await asyncio.sleep(delay=delay)
        chat_ids = await retrieve_inactive_users()
        string = ''
        counter = 0
        if chat_ids:
            for chat_id in chat_ids:
                if int(chat_id['updatedAt'].strftime('%d')) % 2 == 1:
                    await bot.send_message(chat_id=chat_id['tg_id'], text='возможно ты не тупой') 
                    string += ' ' + str(chat_id['tg_id'])
                    counter += 1
            await bot.send_message(chat_id=155269575, text=f'отправлено {counter} людям \n ids: {string}')        
        delay= 86400  # wait every 3600 seconds


# Объект бота
#bot = Bot(token=TOKEN)
# Диспетчер
message = Message
dp = Dispatcher()
async def main():
    await async_main()
    load_dotenv()
    dp.include_router(router)
    time = await find_time()
    asyncio.create_task(coro=scheduler(delay=5))
    poll_object = {'rightans': 0, 'second':'2️⃣ второй', 'third':'3️⃣ третий'}
    await dp.start_polling(bot, poll_object = poll_object)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")    
        