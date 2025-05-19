from aiogram import BaseMiddleware
from aiogram.types import TelegramObject 
from typing import Callable, Dict, Any, Awaitable, Union
import app.database.requests as rq
from aiogram.types import Message
import app.keyboards as kb
import app.handlers 


class Test(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any],) -> Any:
        if handler == app.handlers.cmd_poll or handler == app.handlers.poll_answer_handler:
            self.counter += 1
        #print(handler.new)
        print("Действие до обработчика")
        data['new']= 'neww'
        data["counter"]= self.counter
        print(data)
        if str(type(event)) == "<class 'aiogram.types.poll_answer.PollAnswer'>" or str(type(event)) == "<class 'aiogram.types.poll.Poll'>":
            self.counter += 1
            data["counter"]= self.counter
        print("Действие после обработчика")
        #await event.answer(f"{event.from_user.first_name}. Это действие после обработчика, но до его вывода из функции мидлвари" )
        return await handler(event, data)
