from aiogram import BaseMiddleware
from aiogram.types import TelegramObject 
from typing import Callable, Dict, Any, Awaitable
import app.database.requests as rq
from aiogram.types import Message
import app.keyboards as kb


class Test(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any],) -> Any:
        print(event)
        print("Действие после обработчика")
        #await event.answer(f"{event.from_user.first_name}. Это действие после обработчика, но до его вывода из функции мидлвари" )
        return await handler(event, data)
