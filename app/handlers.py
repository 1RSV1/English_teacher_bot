from aiogram import F, Router, Bot
from aiogram.handlers import BaseHandler
from aiogram.filters.command import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, Video, InputMediaVideo, ForceReply, LabeledPrice, PreCheckoutQuery, input_poll_option, PollAnswer, Poll, MessageEntity, User, FSInputFile, ContentType
import app.keyboards as kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.middlewares import PollAnswerMiddle, PollMiddle, MessageMiddle # импорт мидлвари
import app.database.requests as rq
import datetime
from app.database.requests import  Questions, MyCallback3, Variable, Variable2, Payment, Conditionals, Control
from app.database.models import async_session, Preposition, Test2, Test, Question, Quizes
from sqlalchemy import select, func
from aiogram.methods import DeleteMessage, EditMessageText
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.fsm.storage.redis import RedisStorage
import os
import math
import time, json, string
import random
from aiogram import flags
from collections import Counter
from dotenv import load_dotenv
from typing import  Dict, Any
from openai import OpenAI
from pydub import AudioSegment
load_dotenv()   
bot = Bot(token=os.getenv('TOKEN'))
router = Router()
router.message.middleware(MessageMiddle())
#router.callback_query.middleware(Test())
router.poll_answer.middleware(MessageMiddle())
router.poll.middleware(PollMiddle())
router.message.middleware(ChatActionMiddleware())
from gtts import gTTS



storage = RedisStorage.from_url('redis://default:.g%7B%2BA0La%3B-%3FkSp@92.118.113.44:6379')



@router.message(lambda message: message.voice is not None)
async def handle_all_audios(message: Message):
    await bot.download(message.voice.file_id, f'audio/{message.from_user.id}.mp3')
    client = OpenAI(
     #base_url="https://api.deepseek.com",
     api_key = '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'
    )
    #model = 'whisper-1'
    transcription = client.audio.transcriptions.create(
            model= 'whisper-1',
            file= open(f'audio/{message.from_user.id}.mp3', "rb"),
            response_format="text"  # or "json", "srt", "verbose_json", "vtt"
            )
    data = [{'role': 'user', 'content': transcription}]
    response = client.chat.completions.create(model = 'gpt-4.1-nano', messages = data)
    #await message.answer(text = response.choices[0].message.content) 
    text_gpt = response.choices[0].message.content 
    if text_gpt[0] in string.ascii_letters:
        lang = 'en'
    else:
        lang = 'ru'   
    tts = gTTS(text= text_gpt, lang="en")
    tts.save(f'audio/{message.from_user.id}.mp3') # сохраняет только в mp3
    audio = AudioSegment.from_mp3(f'audio/{message.from_user.id}.mp3') # install ffmpeg on ubuntu
    audio.export(f'audio/{message.from_user.id}.opus', format='opus', codec="libopus", bitrate="64k")   
    voice = FSInputFile(f'audio/{message.from_user.id}.opus', filename = 'gg')
    await bot.send_voice(chat_id = message.from_user.id, voice = voice)  
    
    


@router.message(CommandStart())
async def cmd_start(message: Message):
    if await rq.check_user(message.from_user.id, message.from_user.username):
        await message.answer('Твои статы:' + '\n' + await rq.retrieve_rate(message.from_user.id))
    else:
        await message.answer('Привет, ' + message.from_user.first_name + '. Это бот для изучения английского языка. Выполняй задания, соревнуйся с другими участниками, отслеживай свой прогресс с помощью тестов' + '\n' +  '\n' + await rq.retrieve_rate(message.from_user.id))


@router.message(Command('quiz'), flags={'chat_action': 'typing', 'rate_limit': {'rate': 5}})
@flags.chat_action(initial_sleep=0, action="typing", interval=3)
async def cmd_poll(message: Message):
    first = await rq.retrieve_three_quizes(Quizes ,1, storage = storage)
    option1 = first['option1']
    options = []
    for x, y in first.items():
        if x.startswith('option') and y:
            options.append(input_poll_option.InputPollOption(text= first[x]))
    await message.answer_poll( 
        question= first['question'], 
        open_period = int(first['open_period']), # переделать в цифру в бд
        options= options, 
        correct_option_id= options.index(input_poll_option.InputPollOption(text = option1)),
        type = 'quiz',
        explanation = first['explanation'], 
        explanation_entities = [MessageEntity(type = 'text_mention', offset = 0, length = len(first['explanation']), user = User(id = message.from_user.id, is_bot = False, first_name = 'vad'))]                        
        )
    

@router.poll()
async def poll_answer_handler(poll: Poll):
    voter_count = 0
    rightans = False
    length = poll.explanation_entities[0].length
    for i in range(len(poll.options)):
        if poll.options[i].voter_count:
            voter_count += 1
        if poll.options[i].voter_count == 1 and i == poll.correct_option_id:
            rightans = True
    if  voter_count > 1:
            return   
    if not rightans:
        #if poll.explanation_entities[0].length == len(poll.explanation):
        length = poll.explanation_entities[0].length - 1
        #else:
            #length = poll.explanation_entities[0].length - 2
        
    if poll.question[:3] =='1️⃣':
        await bot.send_poll(chat_id = poll.explanation_entities[0].user.id, open_period = 10, explanation = poll.explanation, 
                            explanation_entities = [MessageEntity(type = 'text_mention', offset = 0, length = length, user = User(id = poll.explanation_entities[0].user.id, is_bot = False, first_name= 'v'), extra_data = {'id': 155269575}), MessageEntity(type = 'custom_emoji', offset = 10, length = 0, custom_emoji_id = '23', extra_data = {'id': 155269575})], 
                            question= '2️⃣ второй', options= [input_poll_option.InputPollOption(text= 'impossible', voter_count = 10), input_poll_option.InputPollOption(text= 'inappropriate', voter_count= 10), input_poll_option.InputPollOption(text= 'inevitable', voter_count= 10)], correct_option_id= 0, type = 'quiz', reply_markup = await rq.markupp(155269575, 33))
    
    elif poll.question[:3] == '2️⃣':
        await bot.send_poll(chat_id = poll.explanation_entities[0].user.id, open_period = 10, explanation = poll.explanation,
                            explanation_entities = [MessageEntity(type = 'text_mention', offset = 0, length = length, user = User(id = poll.explanation_entities[0].user.id, is_bot = False, first_name= 'v'), extra_data = {'id': 155269575}), MessageEntity(type = 'custom_emoji', offset = 10, length = 0, custom_emoji_id = '23', extra_data = {'id': 155269575})], 
                            question= '3️⃣ третий', options= [input_poll_option.InputPollOption(text= 'impossible', voter_count = 10), input_poll_option.InputPollOption(text= 'inappropriate', voter_count= 10), input_poll_option.InputPollOption(text= 'inevitable', voter_count= 10)], correct_option_id= 0, type = 'quiz')
    
    else:
        mistake = len(poll.explanation) - length
        await bot.send_message(chat_id = poll.explanation_entities[0].user.id, text =f"правильно ответил: {3 - mistake}")
    

            # обнуление counter
    #poll.explanation = 'затерли но передали'


    #await bot.send_message(chat_id = poll_answer.user.id, text = f'poll id{poll_answer.poll_id}, option_ids: {poll_answer.option_ids} user {poll_answer.user.id}')
    #await bot.send_poll(chat_id = 155269575, question= f'poll id {poll.id} {poll.question}', options= [input_poll_option.InputPollOption(text= 'impossible', voter_count = 10), input_poll_option.InputPollOption(text= 'inappropriate', voter_count= 10), input_poll_option.InputPollOption(text= 'inevitable', voter_count= 10)], correct_option_id= 0, type = 'quiz')
    #await bot.forward_message(chat_id= '@eng_poll', from_chat_id = poll_answer.user.id, message_id = 4007)

#@router.poll_answer(flags={'NNNNNNNN': 'typing', 'rate_limit': {'rate': 5}, 'message': Message})
#async def poll_answer_handler(poll_answer: PollAnswer):
    #flags = getattr(handler, 'flags', {})
    #message = flags.get('message')
    #print(poll_answer.poll.extra_data)
    #await bot.send_poll(chat_id = 155269575, question= f'poll id', options= [input_poll_option.InputPollOption(text= 'impossible', voter_count = 10), input_poll_option.InputPollOption(text= 'inappropriate', voter_count= 10), input_poll_option.InputPollOption(text= 'inevitable', voter_count= 10)], correct_option_id= 0, type = 'quiz', is_anonymous = False)
    
    
    #await bot.send_message(chat_id = poll_answer.user.id, text = f'poll id{poll_answer.poll_id}, option_ids: {poll_answer.option_ids} user {poll_answer.user.id}')
    #await message.answer_poll(question= 'newer' + str(message.message_id) , options= [input_poll_option.InputPollOption(text= 'impossible', voter_count = 10), input_poll_option.InputPollOption(text= 'inappropriate', voter_count= 10), input_poll_option.InputPollOption(text= 'inevitable', voter_count= 10)], correct_option_id= 0, type = 'quiz', is_anonymous=False)
    #await bot.forward_message(chat_id= '@eng_poll', from_chat_id = poll_answer.user.id, message_id = 4007)




@router.message(Command('rate'))
async def cmd_rate(message: Message):
    await message.answer(text= await rq.retrieve_top_players(message.from_user.id))
 


@router.message(Command('test'))
async def Choose_one(message: Message):
    #data = await rq.retrieve_stars_level_tasklevel_tasktime(message.from_user.id, Users.wordslevel, Users.wordstime)
    task_level = await rq.db_helper(message.from_user.id, task_param = 'test_level_time', command= 'test')
    if task_level == '1':
        await message.answer(text= await rq.three_options_sentence(int(task_level), Test2), reply_markup= await rq.three_options_keyboard('t', int(task_level), Test2))
    else:
        await message.answer('Новый тест пока что недоступен. Дам знать, когда появится')    

@router.callback_query(Control.filter(F.mark == 't'))
async def my_callback(query: CallbackQuery, callback_data: Control):
    if callback_data.ans == '0': # нулевой индекс всегда правильный ответ(лист перемешан)
        callback_data.rightans += 1
        await query.answer("✅✅✅")
    else:
        await query.answer("❌❌❌")

    if callback_data.id%20 == 0:
        await rq.db_helper(query.from_user.id, task_param = 'question_level_time', stars = int(callback_data.rightans * 1.5), level = round(callback_data.rightans/100, 2), task_level = callback_data.id)
        await query.message.edit_text(text=f'Тест пройден. Здесь анализ ответов исходя из  {callback_data.rightans}') # написать функцию
    else:    
        await query.message.edit_text(text= await rq.three_options_sentence(callback_data.id + 1, Test2), reply_markup= await rq.three_options_keyboard('t', callback_data.id + 1, Test2, callback_data.rightans))







#TEST words--------------------------------------------------------------------------------------------------------------------
@router.message(Command('conditionals'))
async def compilesentence(message: Message):
    task_level = True #await rq.db_helper(message.from_user.id, task_param = 'words_level_time', command= 'words_level_time')
    if task_level:
        await message.answer('Выбери пары из левой и правой колонки по смыслу', reply_markup= await rq.test(Test, 1))
    else:
        await message.answer('Новый тест пока что не доступен')  

   
@router.callback_query(Conditionals.filter())
async def my_callback(query: CallbackQuery, callback_data: Conditionals):
    listt = callback_data.keyboard.split(',')
    if  not callback_data.firstans or not callback_data.secondans:
        await query.message.edit_text('Выбери пары из левой и правой колонки по смыслу', reply_markup= await rq.test(Test, callback_data.id, listt, callback_data.firstans, callback_data.secondans, callback_data.rightans, callback_data.falseans))
        await query.answer("...")
    elif int(callback_data.firstans[-1]) == int(callback_data.secondans[-1]) - 4:
        listt.remove(callback_data.firstans)
        listt.remove(callback_data.secondans)
        if len(listt) > 2:
            await query.message.edit_text('Выбери пары из левой и правой колонки по смыслу', reply_markup= await rq.test(Test, callback_data.id, listt, '', '', callback_data.rightans + 1, callback_data.falseans))
            await query.answer("✅✅✅")
        else:
            if str(callback_data.id)[-1] == '0' or str(callback_data.id)[-1] == '5': # если номер теста заканчивается на 0 или 5 question_level_time
                #callback_data.rightans += 1 добавить балл аза последнюю пару
                rightans = callback_data.rightans - callback_data.falseans
                await rq.db_helper(query.from_user.id, task_param = 'words_level_time', command= 'query')
                if str(int(callback_data.id) - 5) > await rq.db_helper(query.from_user.id, task_param = 'words_level_time', command= 'query'):
                    await query.message.edit_text('Урок уже был пройден')
                elif rightans > 0:
                    await rq.db_helper(query.from_user.id, task_param = 'words_level_time', stars = rightans, level = rightans/100, task_level = 5)
                    await query.message.edit_text(f'Урок пройден. Плюс {rightans}⭐') # уровень и время тоже надо записать 
                else:
                    await rq.db_helper(query.from_user.id, task_param = 'words_level_time', task_level = 5)
                    await query.message.edit_text(f'Урок пройден. Звезд не начислено') # уровень и время тоже надо записать
            else:
                await query.message.edit_text('Выбери пары из левой и правой колонки по смыслу', reply_markup= await rq.test(Test, callback_data.id + 1, None, '', '', callback_data.rightans + 1, callback_data.falseans))
                await query.answer("next...")

    else:
        await query.message.edit_text('Выбери пары из левой и правой колонки по смыслу', reply_markup= await rq.test(Test, callback_data.id, listt, '', '', callback_data.rightans, callback_data.falseans + 1))
        await query.answer("❌❌❌")



# Questions logic -------------------------------------------------------------------------------------------------------------------------

@router.message(Command('questions'))
async def compilesentence(message: Message):
    #storage = RedisStorage.from_url('redis://default:.g%7B%2BA0La%3B-%3FkSp@92.118.113.44:6379')
    task_level = True #await rq.db_helper(message.from_user.id, task_param = 'words_level_time', command= 'words_level_time')
    if task_level:
        await message.answer(' ?', reply_markup= await rq.collect_words(id = 1, table = Question, storage = storage))
    else:
        await message.answer('Сегодня ты уже прошел тест. Новый появится завтра') #reply_markup= await kb.two_options(data[2], 'questions'



@router.callback_query(Questions.filter())
async def my_callback(query: CallbackQuery, callback_data: Questions):
    #storage = RedisStorage.from_url('redis://default:.g%7B%2BA0La%3B-%3FkSp@92.118.113.44:6379')
    indexes = callback_data.indexes.split(',')
    current_indexes = callback_data.current_indexes.split(',')
    word = callback_data.word
    if ' ' + word + ' ' in query.message.text or query.message.text.startswith(word + ' '): # протестить word + ' ?' in query.message.text
        current_indexes.remove(callback_data.index)
        newline = query.message.text.replace(word if query.message.text.startswith(word) else ' ' + word, '')
        await query.message.edit_text(text= newline, reply_markup= await rq.collect_words(id = callback_data.id, rightans= callback_data.rightans, indexes = indexes, current_indexes = current_indexes, table = Question, storage = storage))
    else:  
        current_indexes.append(callback_data.index) 
        await query.message.edit_text(text = query.message.text.rstrip('?') +  callback_data.word + ' ?' , reply_markup= await rq.collect_words(id = callback_data.id, rightans= callback_data.rightans, indexes = indexes, current_indexes = current_indexes, table = Question, storage = storage), parse_mode= 'MarkdownV2')
        print(current_indexes, callback_data.indexes)
        if len(indexes) == len(current_indexes) - 1:
            judge = []
            for i in range(len(indexes)):
                judge.append(str(i))

            if judge == current_indexes[1:]:
                await query.answer("✅✅✅")
                callback_data.rightans += 1
            else:
                await query.answer("❌❌❌")    
                
            if callback_data.id % 10 == 0:
                level = await rq.db_helper(query.from_user.id, task_param = 'words_level_time', command= 'questions')
                if callback_data.id > int(level): # будет ли проблема при переходе с 10 на 11 уровень?    
                    await rq.db_helper(query.from_user.id, task_param = 'words_level_time', stars = callback_data.rightans, level = callback_data.rightans/100, task_level = 10)
                    await query.message.edit_text(f'урок закончен. плюс {callback_data.rightans}⭐')
                else:
                        await rq.db_helper(query.from_user.id, task_param = 'words_level_time', stars = callback_data.rightans//2)
                        await query.message.edit_text('урок пройден повторно')   
                #await query.message.edit_text('урок закончен. плюс сколько то денег')
            else:
                await query.message.edit_text(' ?', reply_markup= await rq.collect_words(id = callback_data.id + 1, rightans= callback_data.rightans, table = Question, storage = storage))  
                         
                  

# Делает баланс равным 30 у пользователя       
@router.message((F.text == 'добавить звезды')) 
async def cmd_star(message: Message):
        await rq.update_stars('30', message.from_user.id)
        await message.answer('добавлено 30⭐')   

@router.callback_query(Variable.filter())
async def my_callback(query: CallbackQuery, callback_data: Variable):
    await query.message.edit_text('выбери номер задания', reply_markup= await kb.completed_lessons(callback_data.level, callback_data.mark))

@router.callback_query(Variable2.filter())
async def my_callback(query: CallbackQuery, callback_data: Variable2):
        if callback_data.mark == 'questions':
            await query.message.edit_text(' ?', reply_markup= await rq.inlinebuttons(int(callback_data.level), 0))
        elif callback_data.mark == 'prep':
            number = int(callback_data.level)
            await query.message.edit_text(text= await rq.retrieve_sentense(number), reply_markup= await rq.inlinebuttonss(number))
        elif  callback_data.mark == 'words':
            await query.message.edit_text('Выбери пары из левой и правой колонки по смыслу', reply_markup= await rq.test(int(callback_data.level)* 5 - 4)) 

                               
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
        elif callback_data.mark == 'words': 
            await rq.update_wordstime(datetime.datetime(2025, 4, 4).strftime('%x'), query.from_user.id)
            await query.message.edit_text('урок открыт')    


    



# Prepositions logic -------------------------------------------------------------------------------------------------------------------------
@router.message(Command("prepositions"))
async def learnprep(message: Message):
    task_level = await rq.db_helper(message.from_user.id, task_param = 'question_level_time', command= 'question_level_tim')
    if task_level:
        await message.answer(text= await rq.three_options_sentence(int(task_level), Preposition), reply_markup= await rq.three_options_keyboard('p', int(task_level), Preposition))
    else:
        await message.answer('Сегодня ты уже прошел тест. Новый появится завтра')


@router.callback_query(Control.filter(F.mark == 'p'))
async def my_callback(query: CallbackQuery, callback_data: Control):
    print(callback_data.__dict__)
    if callback_data.ans == '0': # нулевой индекс всегда правильный ответ(лист перемешан)
        callback_data.rightans += 1
        await query.answer("✅✅✅")
    else:
        await query.answer("❌❌❌")

    if callback_data.id%10 == 0:
        await rq.db_helper(query.from_user.id, task_param = 'question_level_time', stars = int(callback_data.rightans * 1.5), level = round(callback_data.rightans/100, 2), task_level = callback_data.id)
        await query.message.edit_text(text=f'Тест пройден. Здесь анализ ответов исходя из  {callback_data.rightans}') # написать функцию
    else:    
        await query.message.edit_text(text= await rq.three_options_sentence(callback_data.id + 1, Preposition), reply_markup= await rq.three_options_keyboard('p', callback_data.id + 1, Preposition, callback_data.rightans))





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
async def find_time():
    appropriate = 720 # время для отправки уведомлений пользователям в минутах
    x = datetime.datetime.now().strftime("%X")
    minutes = int(x[:2])*60 + int(x[3:5])
    if minutes < appropriate:
        return (appropriate - minutes)*60
    elif minutes > appropriate:
        return (1440 - minutes + appropriate)*60
    else:
        return 0
    

@router.message()
async def open_ai(message: Message):
    text = message.text
    
    client = OpenAI(
     #base_url="https://api.deepseek.com",
     api_key = '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'
    )
    model = 'whisper-1'
    data = [{'role': 'user', 'content': text}]
    response = client.chat.completions.create(model = model, messages = data)
    await message.answer(text = response.choices[0].message.content)    
    '''
    tts = gTTS(text=text, lang="en")
    tts.save("audio/output.mp3")
    audio = AudioSegment.from_mp3("audio/output.mp3") # install ffmpeg on ubuntu
    audio.export("audio/outpu.ogg", format='ogg', codec='libvorbis')
    cat = FSInputFile(f'audio/outpu.ogg', filename = 'gg')
    await bot.send_voice(chat_id = message.from_user.id, voice = cat, reply_markup = kb.choice)
    '''