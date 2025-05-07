from aiogram import F, Router, Bot
from aiogram.filters.command import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, Video, InputMediaVideo, ForceReply, LabeledPrice, PreCheckoutQuery
import app.keyboards as kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.middlewares import Test # импорт мидлвари
import app.database.requests as rq
import datetime
from app.database.requests import Prepositions, Questions, MyCallback3, Variable, Variable2, Payment, Testt
from app.database.models import async_session
from app.database.models import  Preposition, Words
from sqlalchemy import select, func
from aiogram.methods import DeleteMessage, EditMessageText
import os
import math
import time
import random
from aiogram import flags
from collections import Counter
   
#bot = Bot(token=os.getenv('TOKEN'))
router = Router()
router.message.middleware(Test())


@router.message(CommandStart())
async def cmd_start(message: Message):
    if await rq.check_user(message.from_user.id):
        await message.answer('Твои статы:' + '\n' + await rq.retrieve_rate(message.from_user.id))
    else:
        await message.answer('Привет, ' + message.from_user.first_name + '. Это бот для изучения английского языка. Выполняй задания, соревнуйся с другими участниками, отслеживай свой прогресс с помощью тестов' + '\n' +  '\n' + await rq.retrieve_rate(message.from_user.id))

@router.callback_query(Variable.filter())
async def my_callback(query: CallbackQuery, callback_data: Variable):
    await query.message.edit_text('выбери номер задания', reply_markup= await kb.completed_lessons(callback_data.level, callback_data.mark))

@router.message(Command('test'))
async def compilesentence(message: Message):
    listt = ['a', 'b', 'c', 'd', 'a', 'b', 'c', 'd']
    await message.answer('выбери пары', reply_markup= await rq.test())

@router.callback_query(Testt.filter())
async def my_callback(query: CallbackQuery, callback_data: Test):
    listt = callback_data.keyboard.split(',')
    if  not callback_data.firstans or not callback_data.secondans:
        await query.message.edit_text('выбери пары', reply_markup= await rq.test(listt, callback_data.firstans, callback_data.secondans))
    else:
        await query.message.edit_text('ты попал в блок валидации')

# Questions logic -------------------------------------------------------------------------------------------------------------------------

@router.message(Command('questions'))
async def compilesentence(message: Message):
    data = await rq.retrieve_stars_level_questionlevel_questiontime(message.from_user.id)
    if datetime.datetime.now().strftime('%x') > data[3]:
        questionlevel = data[2] + '1'
        await message.answer(' ?', reply_markup= await rq.inlinebuttons(int(questionlevel), 0))
        await rq.update_questiontime(datetime.datetime.now().strftime('%x'), message.from_user.id)
    else:
        await message.answer('Сегодня ты уже прошел тест. Новый появится завтра', reply_markup= await kb.two_options(data[2], 'questions'))

@router.callback_query(Variable2.filter())
async def my_callback(query: CallbackQuery, callback_data: Variable2):
        if callback_data.mark == 'questions':
            await query.message.edit_text(' ?', reply_markup= await rq.inlinebuttons(int(callback_data.level), 0))
        elif callback_data.mark == 'prep':
            number = int(str(int(callback_data.level) - 1) + '1')
            await query.message.edit_text(text= await rq.retrieve_sentense(number), reply_markup= await rq.inlinebuttonss(number))

          


@router.callback_query(Questions.filter())
async def my_callback(query: CallbackQuery, callback_data: Questions):
    x = callback_data.keyboard.split(',')
    word = callback_data.word
    if word in query.message.text:
        newline = query.message.text.replace(word if query.message.text.startswith(word) else ' ' + word, '')
        await query.message.edit_text(text= newline, reply_markup= await rq.inlinebuttons2(x, callback_data.numberofquestion, callback_data.rightans))
    else:   
        await query.message.edit_text(text= callback_data.word  + ' ?' if query.message.text == ' ?'  else query.message.text.rstrip('?') +  callback_data.word + ' ?' , reply_markup= await rq.inlinebuttons2(x, callback_data.numberofquestion, callback_data.rightans), parse_mode= 'MarkdownV2')
        listMessage = query.message.text.split(' ')
        if len(listMessage) == len(x):
            rightans = await rq.retrieve_rightans(callback_data.numberofquestion)
            data = await rq.retrieve_stars_level_questionlevel_questiontime(query.from_user.id)
            rightans.pop()
            listMessage.pop()
            #print(rightans)
            #print(listMessage)
            if listMessage == rightans:
                await query.answer("✅✅✅")
                if str(callback_data.numberofquestion)[-1] == '0':
                    if str(callback_data.numberofquestion)[:-1] == str(int(data[2]) + 1): # будет ли проблема при переходе с 10 на 11 уровень? 
                        callback_data.rightans += 1
                        await rq.update_stars_level_questionlevel_questiontime(data[0], data[1], int(data[2]) + 1, datetime.datetime.now().strftime('%x'), callback_data.rightans, query.from_user.id)
                        await query.message.edit_text(f'урок закончен. плюс {callback_data.rightans}⭐')
                    else:
                         await query.message.edit_text('урок пройден повторно')   
                    #await query.message.edit_text('урок закончен. плюс сколько то денег')
                else:
                    callback_data.rightans += 1
                    await query.message.edit_text(' ?', reply_markup= await rq.inlinebuttons(callback_data.numberofquestion + 1, callback_data.rightans))   
            else:
                await query.answer("❌❌❌") 
                if str(callback_data.numberofquestion)[-1] == '0': 
                    if str(callback_data.numberofquestion)[:-1] == str(int(data[2]) + 1):
                        await rq.update_stars_level_questionlevel_questiontime(data[0], data[1], int(data[2]) + 1, datetime.datetime.now().strftime('%x'), callback_data.rightans, query.from_user.id)
                        await query.message.edit_text(f'урок закончен. плюс {callback_data.rightans}⭐')
                    else:
                         await query.message.edit_text('урок пройден повторно')   
                else:
                    await query.message.edit_text(' ?', reply_markup= await rq.inlinebuttons(callback_data.numberofquestion + 1, callback_data.rightans))  

# Делает баланс равным 30 у пользователя       
@router.message((F.text == 'добавить звезды')) 
async def cmd_star(message: Message):
        await rq.update_stars('30', message.from_user.id)
        await message.answer('добавлено 30⭐')   

@router.callback_query(Payment.filter())
async def my_callback(query: CallbackQuery, callback_data: Payment): 
    stars = await rq.retrieve_stars(query.from_user.id)
    if int(stars) >= 20:
        stars = int(stars) - 20
        await rq.update_stars(str(stars), query.from_user.id)
        if callback_data.mark == 'questions':
            await rq.update_questiontime(datetime.datetime(2025, 4, 4).strftime('%x'), query.from_user.id)
            await query.message.edit_text('урок открыт')
        elif callback_data.mark == 'prep': 
            await rq.update_preptime(datetime.datetime(2025, 4, 4).strftime('%x'), query.from_user.id)
            await query.message.edit_text('урок открыт')


    



# Prepositions logic -------------------------------------------------------------------------------------------------------------------------
@router.message(Command("prepositions"))
async def learnprep(message: Message):
    number = await rq.not_randforsentense(message.from_user.id)
    if not number:
        data = await rq.retrieve_stars_level_preplevel_preptime(message.from_user.id)
        await message.answer('Сегодня ты уже прошел тест. Новый появится завтра', reply_markup= await kb.two_options(data[2], 'prep'))
    else:        
        await message.answer(text= await rq.retrieve_sentense(number), reply_markup= await rq.inlinebuttonss(number))
        await rq.update_preptime(datetime.datetime.now().strftime('%x'), message.from_user.id)  


@router.callback_query(Prepositions.filter())
async def my_callback_foo(query: CallbackQuery, callback_data: Prepositions):      
    async with async_session() as session:
        #prep = await session.scalar(select(Preposition.prep).where(Preposition.id == callback_data.id))
        # придумать защиту от перебора по всем заданиям
        next_id = callback_data.id + 1
        if callback_data.b == callback_data.p:
            callback_data.rightans += 1
            await query.answer("✅✅✅")
            if str(callback_data.id)[-1] == '0':
                data = await rq.retrieve_stars_level_preplevel_preptime(query.from_user.id)
                if str(callback_data.id)[:-1] == str(int(data[2]) + 1): # будет ли проблема при переходе с 10 на 11 уровень? 
                    await rq.update_stars_level_preplevel_preptime(data[0], data[1], int(data[2]) + 1, datetime.datetime.now().strftime('%x'), callback_data.rightans, query.from_user.id)        
                    await query.message.edit_text(f'урок закончен. плюс {callback_data.rightans}⭐')
                else:
                    await query.message.edit_text('урок пройден повторно')
            else:
                await query.message.edit_text(text= await rq.retrieve_sentense(next_id), reply_markup= await rq.inlinebuttonss(next_id, callback_data.rightans))  

        else:
            await query.answer("❌❌❌")
            if str(callback_data.id)[-1] == '0':
                data = await rq.retrieve_stars_level_preplevel_preptime(query.from_user.id)
                if str(callback_data.id)[:-1] == str(int(data[2]) + 1): # будет ли проблема при переходе с 10 на 11 уровень? 
                    await rq.update_stars_level_preplevel_preptime(data[0], data[1], int(data[2]) + 1, datetime.datetime.now().strftime('%x'), callback_data.rightans, query.from_user.id)        
                    await query.message.edit_text(f'урок закончен. плюс {callback_data.rightans}⭐')
                else:
                    await query.message.edit_text('урок пройден повторно')
            #desc = await session.scalar(select(Preposition.description).where(Preposition.id == callback_data.r)) 
            else:   
                await query.message.edit_text(text= await rq.retrieve_sentense(next_id), reply_markup= await rq.inlinebuttonss(next_id, callback_data.rightans))








#Слоты--------------------------------------------------------------------------------------------------------------------------------------
@router.message(Command("slots"))
async def openkeyboard(message: Message):
    stars = await rq.retrieve_stars(message.from_user.id)
    if stars == '0':
        await message.answer('у тебя закончились звезды ⭐')
    else:
        await message.answer( stars + ' ⭐ доступно ', reply_markup=await kb.keyBoard(stars, str(message.from_user.id))) # если все таки зашел с нолем- выкинь его из миниапп

@router.message((F.web_app_data)) 
async def cmd_star(message: Message):
    if message.web_app_data.data != 'звезды закончились':
        await rq.update_stars(message.web_app_data.data, message.from_user.id)
        await message.answer(message.web_app_data.data+'⭐' + ' твои' )  
    else:
        #await rq.update_stars('0', message.from_user.id)
        await message.answer(message.web_app_data.data)

#Команда на оплату и функция на возврат оплаты----------------------------------------------------------
@router.message(Command('pay'))
async def create_invoice(msg: Message):
    Upscale = LabeledPrice(label='Одна покупка', amount=1)

    await bot.send_invoice(
        msg.chat.id,
        title="One little buy",
        description="One little buy",
        provider_token="",
        currency="XTR",
        photo_url="https://mihailgok.ru/upscale.jpg",
        photo_width=3600,
        photo_height=2338,
        photo_size=262000,
        is_flexible=False,
        prices=[Upscale],
        start_parameter="one-upscale",
        payload="one-upscale"
    )


@router.pre_checkout_query()
async def checkout_handler(checkout_query: PreCheckoutQuery):
    await checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def star_payment(msg: Message, bot: Bot):
    '''
    await bot.refund_star_payment(
        msg.chat.id,
        msg.successful_payment.telegram_payment_charge_id,
    )
    '''
    await msg.answer(f"Your transaction id: {msg.successful_payment.telegram_payment_charge_id}")

@router.message(Command('paysupport'))
async def create_invoice(message: Message):
    await message.answer(' инструкция об оплате ⭐' ) 


# НЕ ИСПОЛЬЗУЕТСЯ-------------------------------------------------------------------------

class SomeClass(StatesGroup): # FSM
    translation = State()
    number = State()
    uncountable = State()
    word = State()
    trans = State()
    list = State()

#@router.callback_query(MyCallback.filter())
async def my_callback_foo(query: CallbackQuery, callback_data: Prepositions):      
    if callback_data.exit != '':
        rate = round(callback_data.rightans /callback_data.counter * 100, 0)
        await query.message.edit_text(text= f'процент правильных ответов ={rate}% ')
        return
    async with async_session() as session:
        prep = await session.scalar(select(Preposition.prep).where(Preposition.id == callback_data.r))
        max = await session.scalar(select(func.max(Preposition.id)))
        if callback_data.r == max:
            rate = round(callback_data.rightans / callback_data.counter * 100, 2)
            await query.message.edit_text(text= f'Все задания пройдены\nпроцент правильных ответов ={rate}% ')
            return
        rand = callback_data.r + 1
        if prep == callback_data.b:
            callback_data.rightans += 1
            callback_data.counter += 1
            await query.answer("✅✅✅")
            if callback_data.counter%10 == 0:
                await query.message.edit_text(text= '10 выполнено, продолжить?', reply_markup =await kb.settings(callback_data.b, rand, callback_data.rightans, callback_data.counter))
            else:      
                await query.message.edit_text(text= await rq.retrieve_sentense(rand), reply_markup= await rq.inlinebuttonss(rand, callback_data.rightans, callback_data.counter)) 
                

        else:
            await query.answer("❌❌❌")
            callback_data.counter += 1
            desc = await session.scalar(select(Preposition.description).where(Preposition.id == callback_data.r))    
            await query.message.edit_text(text= desc, reply_markup =await kb.settings(callback_data.b, rand, callback_data.rightans, callback_data.counter))

#@router.callback_query(MyCallback3.filter()) 
async def learnprep(query: CallbackQuery, callback_data: MyCallback3):
    rand = callback_data.r
    if query.message.text == '10 выполнено, продолжить?':
        await query.message.edit_text(text= await rq.retrieve_sentense(rand), reply_markup= await rq.inlinebuttonss(rand, callback_data.rightans, callback_data.counter))
    elif callback_data.counter%10 == 0:
        await query.message.edit_text(text= '10 выполнено, продолжить?', reply_markup =await kb.settings('', str(rand), callback_data.rightans, callback_data.counter))
    else:
        await query.message.edit_text(text= await rq.retrieve_sentense(rand), reply_markup= await rq.inlinebuttonss(rand, callback_data.rightans, callback_data.counter))

# перенос данных из одной бд в другую
@router.message(Command('table'))
async def somereg(message: Message):
    table = await rq.retrieve_table()
    print(table)
    await rq.write_table(table)
    await message.answer("выполнено") 


# СОСТОЯНИЯ НА ДОБАВЛЕНИЕ НЕИСЧИСЛЯЕМЫХ СЛОВ
@router.message(F.text == "write Uncountable")
async def somereg(message: Message, state: FSMContext):
    await state.set_state(SomeClass.uncountable)
    await message.answer("добавьте слова")

@router.message(SomeClass.uncountable)
async def somereg1(message: Message, state: FSMContext):
    await state.update_data(uncountable = message.text)
    await state.set_state(SomeClass.translation)
    await message.answer("добавьте перевод")    

@router.message(SomeClass.translation, F.text)
async def somereg1(message: Message, state: FSMContext):
    await state.update_data(translation = message.text)
    data = await state.get_data()
    await rq.write_words(data["uncountable"], data["translation"])
    await state.clear()
    await message.answer("добавлено")    



# СОСТОЯНИЕ НА ДОБАВЛЕНИЕ id    
@router.message(Command("addid"))
async def somereg(message: Message, state: FSMContext):
    await state.set_state(SomeClass.number)
    await message.answer("добавьте id пользователя")

@router.message(SomeClass.number)
async def somereg5(message: Message, state: FSMContext):
    await state.update_data(number = message.text)
    data = await state.get_data()
    if await rq.add_user(data["number"]):
        await message.answer("добавлено")
        await state.clear()       
    else: 
        await message.answer("пользователь уже добавлен")
        await state.clear()


no_duplicate2 = []
@router.message(F.text == "Learn words")
async def takeoutfromdb1(message: Message, state: FSMContext):
    async with async_session() as session:
        await state.set_state(SomeClass.word)
        max = await session.scalar(select(func.max(Words.id)))
        if len(no_duplicate2) < max:
            rand = await rq.randforsentense(Words.id)
            while rand in no_duplicate2:
                rand = await rq.randforsentense(Words.id)
            no_duplicate2.append(rand)    
            list = await rq.retrieve_word(Words.word, rand)
            list2 = await rq.retrieve_word(Words.translation, rand)
            await state.update_data(list = list, list2 = list2)
            await message.answer(text = list[0], reply_markup= ForceReply())
        else:  
            no_duplicate2.clear()
            await message.answer('слова закончились')
            
# reply_markup= ForceReply(input_field_placeholder= 'Write translation') выше 
    

@router.message(SomeClass.word)
async def takeoutfromdb(message: Message, state: FSMContext):
    await state.update_data(word = [message.text, message.message_id])
    data = await state.get_data()
    time.sleep(5)
    #await bot.delete_message(chat_id=155269575, message_id= data['word'][1])
    if data['word'][0].casefold() in data['list2']:
        await state.clear()
        await takeoutfromdb1(message, state)
    else: 
        await state.clear()   
        await message.answer(f"Варианты правильного перевода: {' '.join(data['list2'])}")     


# Get filter result as handler argument
'''
@router.message(F.text.as_('var')) 
async def cmd_star(message: Message, var):
    await message.answer("любой текст : " + var)
'''    

# if we catch the result by first handler and have a match with another, the next wont be working
'''
@router.message(F.date.func(lambda date: date.strftime("%X") > '09:00:00'))
async def cmd_start(message: Message):
    await message.answer(text= "hello", reply_markup= kb.main)
'''            