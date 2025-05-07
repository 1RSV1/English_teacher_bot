from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import datetime
import app.database.requests as rq
from aiogram.types.web_app_info import WebAppInfo

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = "Learn words"),KeyboardButton(text = "Uncountable words")],
                                     [KeyboardButton(text = "Learn prepositions"), 
                                      KeyboardButton(text = "/admin")] ], resize_keyboard= True, input_field_placeholder= "Choose the button")

admin = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = "write Uncountable")],[KeyboardButton(text = "Крутить", web_app= WebAppInfo(url = "https://ff.engbot.ru") )],
                                     [KeyboardButton(text = "кнопка 2"), 
                                      KeyboardButton(text = "back to main")] ], resize_keyboard= True, input_field_placeholder= "Choose the button")

emptykeyboard = ReplyKeyboardMarkup(keyboard= [[]], input_field_placeholder= 'Write translation')

#одно значение будет истиным, два остальных ложные с пояснением в отдельном хэндлере, где будет предложение продолжить?
choice = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="название кнопки", callback_data="response"), 
                                                InlineKeyboardButton(text="название кнопки", callback_data="response"), 
                                                InlineKeyboardButton(text="название кнопки", callback_data="response")]])

async def settings(b, r, rightans, counter):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="continue", callback_data=rq.MyCallback3(r= r, rightans= rightans, counter= counter).pack()))
    keyboard.add(InlineKeyboardButton(text="exit", callback_data=rq.MyCallback(b= b, r= r, rightans= rightans, counter= counter, exit= 'exit').pack()))
    return keyboard.adjust(2).as_markup()

async def two_options(leveloflesson, mark):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="повторить пройденное", callback_data=rq.Variable(level= leveloflesson, mark= mark).pack()))
    keyboard.add(InlineKeyboardButton(text="открыть за 20⭐", callback_data= rq.Payment(mark= mark).pack()))
    return keyboard.adjust(2).as_markup()

async def completed_lessons(leveloflesson, mark):
    keyboard = InlineKeyboardBuilder()
    for level in range(int(leveloflesson)):
        keyboard.add(InlineKeyboardButton(text=str(level + 1), callback_data=rq.Variable2(level= str(level) + '1', mark= mark).pack()))
    return keyboard.adjust(6).as_markup()



buttons = ["1", "Обновить" ] # InlineKeyboardBuilder
async def add_day(p):
    buttons.insert(-1, str(p))
    return buttons
   
    
async def keyBoard(stars, tg_id):
    keyboard= ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text = "Крутить", web_app= WebAppInfo(url = "https://ff.engbot.ru/slots/" + stars + '/' + tg_id)))
    return keyboard.as_markup(resize_keyboard= True)
       


async def inlinebuttons(): # создание клавиатуры через функцию исходя из данных из бд (BUILDER)
    keyboard = InlineKeyboardBuilder()
    for button in buttons[:-1]:     
        keyboard.add(InlineKeyboardButton(text = button, callback_data= button )) 
    for button in buttons[-1:]:
        keyboard.add(InlineKeyboardButton(text = button, callback_data= "res"))    
            
    return keyboard.adjust(2).as_markup()     #adjust(2).


