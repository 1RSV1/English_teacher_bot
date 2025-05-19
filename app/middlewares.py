from aiogram import BaseMiddleware
from aiogram.types import TelegramObject , PollAnswer, Poll
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
        print(type(event))
        if type(event) == Message:
            if data['command'].command == 'poll':
                
                data["counter"]= 0
                
        print("Действие до обработчика")
        
        if type(event) == PollAnswer or type(event) == Poll:
            self.counter += 1
            if self.counter == 2:
                 self.counter = 0
            data["counter"]= self.counter   
        print("Действие после обработчика")
        #await event.answer(f"{event.from_user.first_name}. Это действие после обработчика, но до его вывода из функции мидлвари" )
        print(data["counter"]) 
        return await handler(event, data)
