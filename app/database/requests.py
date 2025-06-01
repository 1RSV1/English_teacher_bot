from app.database.models import async_session, async_session2, engine
from app.database.models import   Preposition,  Users, Question, Test, Test2
from sqlalchemy import select, update, delete, func
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random, datetime
from aiogram.filters.callback_data import CallbackData
from typing import Any
import json
from aiogram.fsm.storage.redis import RedisStorage


    
              
class Questions(CallbackData, prefix="my"):
    id: int
    word: str
    indexes: str  
    index: str 
    current_indexes: str
    rightans: int

class MyCallback3(CallbackData, prefix="m"):
   r: int
   rightans: int
   counter: int

class Variable(CallbackData, prefix='ma'):
    level: str
    mark: str    

class Variable2(CallbackData, prefix='m'):
    level: str        
    mark: str

class Payment(CallbackData, prefix='pay'):
    mark: str 

class Conditionals(CallbackData, prefix='test'):
    id: int
    keyboard: str 
    firstans: str
    secondans: str  
    rightans: int
    falseans: int 


class Control(CallbackData, prefix='c'):
    mark: str 
    id: int
    ans: str    
    rightans: int    

async def markupp(id, info) :
    return   


async def three_options_sentence(id, table):
    async with async_session() as session:
        sentence = await session.scalar(select(table.sentence).where(table.id == id))
        return sentence

async def three_options_keyboard(mark, id, table, rightans= 0, adjust = 1):
    list = await retrieve_datalist(table, id) #<class 'app.database.models.Preposition'>
    if isinstance(table(), Preposition):
        adjust = len(list) 
    random.shuffle(list)
    keyboard = InlineKeyboardBuilder()
    for item in list:
        keyboard.add(InlineKeyboardButton(text = item[:-1], callback_data= Control(mark = mark, id= id, ans= item[-1], rightans= rightans).pack())) 
    print(keyboard)           
    return keyboard.adjust(adjust).as_markup()

    
       

async def test(table, id, listt='', firstans= '', secondans= '', rightans= 0, falseans= 0, storage = RedisStorage):
    #async with async_session() as session:
        value = await storage.redis.get(name = id)
        if value:
            list = json.loads(value.decode())
        else:    
            list = await retrieve_datalist(table, id)
        val = json.dumps(list)
        await storage.redis.set(name = id, value = val, ex = 60) # проверить
        if not listt:    
            listt2 = list[len(list)//2:]
            list = list[:len(list)//2]
            random.shuffle(listt2)
            list += listt2 
        else:
            newlist = []
            for i in listt:
                newlist.append(list[int(i)])
            list = newlist 
        listindex = []
        for item in list:
                listindex.append(item[-1])
                x = ','.join(listindex)      
        keyboard = InlineKeyboardBuilder()
        for i in range(len(list)//2):
            keyboard.add(InlineKeyboardButton(text = list[i][:-1], callback_data= Conditionals(id= id, keyboard= x, firstans= list[i][-1], secondans= secondans, rightans= rightans, falseans= falseans).pack()))
            keyboard.add(InlineKeyboardButton(text = list[len(list)//2 + i][:-1], callback_data= Conditionals(id= id, keyboard= x, firstans=firstans, secondans= str(list[len(list)//2 + i][-1]), rightans= rightans, falseans= falseans).pack()))
        return keyboard.adjust(2).as_markup()

async def retrieve_datalist(table, id):
    async with async_session() as session:
        listt = []
        info = await session.execute(select(table).where(table.id == id)) 
        db_string = info.scalars().first().__dict__
        #db_string = db_string.__dict__
        db_string = {k: db_string[k] for k in sorted(db_string)} # сортировка словаря по ключам (колонки в бд должны быть с номерами) словарь из класса приходит неотсортированный
        #print(db_string)
        for key, value in db_string.items():
            if value == None or type(value) == int or key.startswith('_') or key == 'sentence':
                continue
            listt.append(value)
        for i in range(len(listt)):
            listt[i] += str(i)   
        #print(listt)         
        return  listt   

async def retrieve_three_quizes(table, id, tg_id, storage = RedisStorage):
    async with async_session() as session:
        d = {}
        info = await session.execute(select(table).where(table.id >= id).where(table.id < id + 3)) 
        db_string_list = info.scalars().all()
        first = db_string_list[0].__dict__
        db_string_list[1].__dict__.pop('_sa_instance_state') # чтобы словарь упаковать в json
        db_string_list[2].__dict__.pop('_sa_instance_state') # чтобы словарь упаковать в json
        d['second'] = db_string_list[1].__dict__
        d['third'] = db_string_list[2].__dict__
        d['ans'] = 0
        await storage.redis.set(name = str(tg_id)+ '_quiz', value = json.dumps(d), ex = 60)
        
        return first
    

    
 




# Question queries---------------------------------------------------------------------------------------------------------------
async def collect_words(id, rightans= 0, list = None, indexes = None, current_indexes = '', table = None, storage = RedisStorage):
    #async with async_session() as session:
        value = await storage.redis.get(name = id)
        if value:
            list = json.loads(value.decode())
        else:    
            list = await retrieve_datalist(table, id)
        val = json.dumps(list)
        await storage.redis.set(name = id, value = val, ex = 10)
        if indexes:
            sorted_list = []
            for i in indexes:
                sorted_list.append(list[int(i)])
            list = sorted_list            
        else:
            indexes = []          
            random.shuffle(list)
            for item in list:
                indexes.append(item[-1])
        x = ','.join(indexes)
        current_indexes = ','.join(current_indexes)
        keyboard = InlineKeyboardBuilder()
        for button in list:   
                keyboard.add(InlineKeyboardButton(text = button[:-1], callback_data= Questions(id = id, word= button[:-1], indexes = x, index = button[-1], current_indexes = current_indexes, rightans = rightans).pack()))          
        return keyboard.adjust(3).as_markup()     #adjust(2)    

  

   





#User registration----------------------------------------------------------------------------------------------------        
        
async def check_user(tg_id, tg_username):
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id == tg_id))
        if not user:
            session.add(Users(tg_id = tg_id, tg_username = tg_username))
            await session.commit()
            return False
        else:
            return True   
# можно объединить 
async def retrieve_rate(id):
    async with async_session() as session:
        listt = []
        sentense = await session.execute(select(Users.stars, Users.level).where(Users.tg_id == id)) 
        for tupl in sentense:
            for t1 in tupl:
                listt.append(t1)
        level = str(listt[1]).split('.')        
        return f"Stars: {str(listt[0])}\nLevel: {level[0]} | {int(level[1])}%" 
             
# Перенос инфы из одной таблицы в другую из разных бд-------------------------------------------------------------------------------------------------
async def retrieve_table():
    async with async_session2() as session2:
        listt = []
        sentense = await session2.execute(select(Preposition))
        new = sentense.scalars()
        for i in new:
            listt.append(Preposition(part1 = i.part1, prep = i.prep, part2 = i.part2, description = i.description))
        return listt     

async def write_table(listt):
    async with async_session() as session:
        session.add_all(listt)
        await session.commit()
            




# Используется при открытии слотов-----------------------------------------------------------------------------------------------
async def retrieve_stars(id):
    async with async_session() as session:
        stars = await session.scalar(select(Users.stars).where(Users.tg_id == id))
        return stars    
#Добавляет звезды в хэндлере на добавление звезд------------------------------------------------------------------------------------
async def update_stars(stars, tg_id):
    async with async_session() as session:
        #users = Users
        #users.stars = stars
        #conn = engine.connect()
        #stmt = Users.update().values(stars=Users.stars + 300).where(Users.tg_id == tg_id)
        #session.query(Users).filter(Users.tg_id == tg_id).update({'stars': stars})
        await session.execute(update(Users).where(Users.tg_id == tg_id).values(stars=stars))
        await session.commit()
        #conn.execute(stmt)



########################################################################################################################################################################################
async def db_helper(tg_id, task_param = '', command= None, stars = 0, level = 0, task_level = 0): #stars, level, wordslevel, wordstime, rightans,  tg_id
    #instance = await session.get(Users, id) <app.database.models.Users object at 0x000001E98C6D7940>
    async with async_session() as session: 
        info = await session.execute(select(Users).where(Users.tg_id == tg_id)) 
        db_string = info.scalars().first()
        level_time = getattr(db_string, task_param)
        if command: # старт задания на команду
            if db_string.is_subscribed: # если подписан, новые задания без ограничений
                return level_time[:-9]
            else:
                if datetime.datetime.now().strftime("%x") == level_time[-8:] and command == task_param: 
                    return False
                setattr(db_string, task_param, level_time[:-8] + datetime.datetime.now().strftime("%x")) # повторно команда сработает через день 
                await session.commit()
                return level_time[:-9]  
        else:     
            setattr(db_string, task_param, str(int(level_time[:-9]) + task_level) + level_time[-9:]) # запись старс левел и уровня таска, функция без команды
            db_string.stars += stars
            db_string.level += round(level, 2)
            db_string.updatedAt = datetime.datetime.now() 
            await session.commit()        

#НЕ ИСПОЛЬЗУЕТСЯ---------------------------------------------------------------------------------------------------------------------------------------

async def write_words(word, translation):
    async with async_session() as session:
        session.add(Uncountable(word = word, translation = translation))
        await session.commit()

async def delete_table():
    async with async_session() as session:
        session.delete()
        await session.commit()

async def randforsentense(tableparam):
    async with async_session() as session:
        max = await session.scalar(select(func.max(tableparam)))
        rand = random.randint(1, max)
        return rand
    
# TRANSLATION
async def retrieve_word(column, rand):
    async with async_session() as session:
        word = await session.scalar(select(column).where(Words.id == rand))
        return word.split(', ')    
    

'''
async def retrieve_photo(p):
    async with async_session() as session:
        fileids = await session.scalars(select(Picturee.name).where(Picturee.day == p))
        listt = []
        for file in fileids:
            if not listt:
                if file.startswith("AgACAgIAA"):
                    listt.append(InputMediaPhoto(media= file, caption= f"День {p}", show_caption_above_media= True))
                else:
                    listt.append(InputMediaVideo(media= file, caption= f"День {p}", show_caption_above_media= True))


            elif file.startswith("AgACAgIAA"):
                 listt.append(InputMediaPhoto(media= file, show_caption_above_media= True))
            else:
                 listt.append(InputMediaVideo(media= file, show_caption_above_media= True))
                

        return listt    
'''    

# UNCOUNTABLE
async def retrieve_words():
    async with async_session() as session:
        text = ''
        words = await session.execute(select(Uncountable.word, Uncountable.translation))
        for word in words:
            (a, b) = word
            text += a + ' - ' + b + "\n"

        return text 
    
async def retrieve_inactive_users():
      twelve_days_earlier = datetime.datetime.now() - datetime.timedelta(days = 12)
      two_days_earlier = datetime.datetime.now() - datetime.timedelta(days = 2)
      async with async_session() as session:
          listt = []
          users_object = await session.execute(select(Users.tg_id, Users.updatedAt).where(Users.updatedAt >= twelve_days_earlier).where(Users.updatedAt <= two_days_earlier))  
          for tupl in users_object:
            dict = {'tg_id': tupl[0], 'updatedAt': tupl[1]}
            listt.append(dict)
          return listt    

async def retrieve_top_players(tg_id):
    async with async_session() as session:
        message = ''
        users_object = await session.execute(select(Users.tg_id, Users.tg_username, Users.level).order_by(Users.level.desc())) 
        top = 1
        is_in = False
        for tupl in users_object:
            if top < 6:  
                if tupl[0] == tg_id:
                    is_in = True    
                message += f'{tupl[1]} level: {tupl[2]} \n'  
                top += 1
            else:
                if not is_in:
                    if tupl[0] == tg_id:
                        return f'{message}\nты на {top} месте'
                top += 1  
        return message   
