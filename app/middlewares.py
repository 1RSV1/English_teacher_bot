from aiogram import BaseMiddleware
from aiogram.types import TelegramObject , PollAnswer, Poll, Message
from typing import Callable, Dict, Any, Awaitable, Union
import app.database.requests as rq
import app.keyboards as kb
import app.handlers 


class MessageMiddle(BaseMiddleware):
    
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any],) -> Any:
            #print(data)

            #data['message'] = data['handler'].flags['message']
            #await self.message.answer( text = 'some answer')
            #data['counter'] = 1
            #print(data['handler'].flags['message'])
            return await handler(event, data)
    
class PollAnswerMiddle(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any],) -> Any:
        data['counter'] += 1
        print(data['counter'])
        return await handler(event, data)  

class PollMiddle(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0
        self.total_counter = 0

    async def __call__(self,
                    handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                    event: TelegramObject,
                    data: Dict[str, Any],) -> Any:
        print(data)
        '''
        #self.counter += 1        
        data['counter'] = self.counter
        result = await handler(event, data)
        if result:
             self.counter += 1
        self.total_counter += 1
        if self.total_counter == 3:
             self.counter = 0
             self.total_counter = 0
        '''     
        result = await handler(event, data)  
        #print("Действие после обработчика")
        #await event.answer(f"{event.from_user.first_name}. Это действие после обработчика, но до его вывода из функции мидлвари" )
        #print(data["counter"]) 
        return result     
