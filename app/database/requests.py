from app.database.models import async_session, async_session2, engine
from app.database.models import  Uncountable, Preposition, Words, Users, Question, Test, Test2
from sqlalchemy import select, update, delete, func
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random, datetime
from aiogram.filters.callback_data import CallbackData
from typing import Any

class instance():
    stars: int
    level: float

class Prepositions(CallbackData, prefix="myy"):
    b: str
    p: str
    id: int
    rightans: int
    
              
class Questions(CallbackData, prefix="my"):
    word: str
    keyboard: str   
    numberofquestion: int
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

class Testt(CallbackData, prefix='test'):
    id: int
    keyboard: str 
    firstans: str
    secondans: str  
    rightans: int
    falseans: int 

class Control(CallbackData, prefix='c'):
    id: int
    ans: str    
    rightans: int

async def markupp(id, info) :
    return   


async def three_options_sentence(id, table):
    async with async_session() as session:
        sentence = await session.scalar(select(table.sentence).where(table.id == id))
        return sentence

async def three_options_keyboard(id, table, rightans= 0):
    list = await retrieve_datalist2(id, table)
    random.shuffle(list)
    keyboard = InlineKeyboardBuilder()
    for item in list:
        keyboard.add(InlineKeyboardButton(text = item[:-1], callback_data= Control(id= id, ans= item[-1], rightans= rightans).pack()))        
    return keyboard.adjust(1).as_markup()

    

async def retrieve_datalist2(id, table):
    async with async_session() as session:
        listt = []
        sentense = await session.execute(select(table.p1, table.p2, table.p3, table.p4, table.p5).where(table.id == id)) 
        for tupl in sentense:
            for t1 in tupl:
                if t1 == None:
                    continue
                listt.append(t1)
        for i in range(len(listt)):
            listt[i] += str(i)        
        return  listt   

       

async def test(id, listt='', firstans= '', secondans= '', rightans= 0, falseans= 0):
    #async with async_session() as session:
        list = await retrieve_datalist(id)
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
            keyboard.add(InlineKeyboardButton(text = list[i][:-1], callback_data= Testt(id= id, keyboard= x, firstans= list[i][-1], secondans= secondans, rightans= rightans, falseans= falseans).pack()))
            keyboard.add(InlineKeyboardButton(text = list[len(list)//2 + i][:-1], callback_data= Testt(id= id, keyboard= x, firstans=firstans, secondans= str(list[len(list)//2 + i][-1]), rightans= rightans, falseans= falseans).pack()))
        return keyboard.adjust(2).as_markup()

async def retrieve_datalist(id):
    async with async_session() as session:
        listt = []
        sentense = await session.execute(select(Test.p1, Test.p2, Test.p3, Test.p4, Test.p5, Test.p6, Test.p7, Test.p8).where(Test.id == id)) 
        for tupl in sentense:
            for t1 in tupl:
                if t1 == None:
                    continue
                listt.append(t1)
        for i in range(len(listt)):
            listt[i] += str(i)        
        return  listt   

# PREPOSITIONS
async def not_randforsentense(id):
    async with async_session() as session:
        listt = []
        data = await session.execute(select(Users.preplevel, Users.preptime).where(Users.tg_id == id))
        for tupl in data:
            for t1 in tupl:
                listt.append(t1)
        
        if datetime.datetime.now().strftime('%x') <= listt[1]:
            return False
        if listt[0] == '0':
            number = 1
        else:
            number = int(listt[0]) * 10 + 1    
        return number    
    
async def retrieve_sentense(id):
    async with async_session() as session:
        listt = []
        sentense = await session.execute(select(Preposition.part1, Preposition.part2).where(Preposition.id == id)) 
        for tupl in sentense:
            for t1 in tupl:
                listt.append(t1)
        return f"{listt[0]}   ...   {listt[1]}"
    
async def inlinebuttonss(id, rightans= 0):
    async with async_session() as session:
        keyboard = InlineKeyboardBuilder()
        prep = await session.scalar(select(Preposition.prep).where(Preposition.id == id))
        prepositions = ['at', 'to', 'for', 'in', 'with', 'without', 'into',]
        final = []
        final.append(prep)
        while len(final) != 3:
            r = random.choice(prepositions)
            if r in final:
                continue
            else:
                final.append(r)
        random.shuffle(final)
        for button in final:     
            keyboard.add(InlineKeyboardButton(text = button, callback_data= Prepositions(b= button, p= prep, id= id, rightans= rightans).pack()))          
        return keyboard.adjust(3).as_markup()     #adjust(2)        

async def retrieve_stars_level_preplevel_preptime(id):
    async with async_session() as session:
        listt = []
        questionlevel = await session.execute(select(Users.stars, Users.level, Users.preplevel, Users.preptime).where(Users.tg_id == id))
        for tupl in questionlevel:
            for t1 in tupl:
                listt.append(t1)
        return listt    

async def update_stars_level_preplevel_preptime(stars, level, preplevel, preptime, rightans,  tg_id):
    async with async_session() as session:
        #listt = []
        #info = await session.execute(select(Users.stars, Users.level).where(Users.tg_id == tg_id)) добавь старс и левел в параметры
        #for tupl in info:
            #for t1 in tupl:
                #listt.append(t1)
        await session.execute(update(Users).where(Users.tg_id == tg_id).values(stars = str(int(stars)+ rightans), level = str(float(level) + rightans/100), preplevel=str(preplevel), preptime = preptime))
        await session.commit()    

async def update_preptime(preptime, tg_id):
    async with async_session() as session:
        await session.execute(update(Users).where(Users.tg_id == tg_id).values(preptime = preptime))
        await session.commit()


# Question queries---------------------------------------------------------------------------------------------------------------
async def inlinebuttons(n, rightans):
    async with async_session() as session:
        keyboard = InlineKeyboardBuilder()
        words = await session.execute(select(Question.part1, Question.part2, Question.part3, Question.part4, Question.part5, Question.part6,).where(Question.id == n))
        listt = []
        for tupl in words:
            for t1 in tupl:
                if t1 == None:
                    continue
                else:
                    listt.append(t1)           
        random.shuffle(listt)
        x = ','.join(listt)
        for button in listt:   
                keyboard.add(InlineKeyboardButton(text = button, callback_data= Questions(word= button, keyboard= x, numberofquestion= n, rightans = rightans).pack()))          
        return keyboard.adjust(3).as_markup()     #adjust(2)    

async def inlinebuttons2(list, n, rightans):
        x = ','.join(list)
        keyboard = InlineKeyboardBuilder()
        for button in list:     
                keyboard.add(InlineKeyboardButton(text = button, callback_data= Questions(word= button, keyboard= x, numberofquestion= n, rightans = rightans).pack()))          
        return keyboard.adjust(3).as_markup()     #adjust(2)  

async def retrieve_rightans(id):
    async with async_session() as session:
        rightans = await session.scalar(select(Question.fullquestion).where(Question.id == id))
        return rightans.split(' ')  

async def retrieve_stars_level_questionlevel_questiontime(id):
    async with async_session() as session:
        listt = []
        questionlevel = await session.execute(select(Users.stars, Users.level, Users.questionlevel, Users.questiontime).where(Users.tg_id == id))
        for tupl in questionlevel:
            for t1 in tupl:
                listt.append(t1)
        return listt    

async def update_stars_level_questionlevel_questiontime(stars, level, questionlevel, questiontime, rightans,  tg_id):
    async with async_session() as session:
        #listt = []
        #info = await session.execute(select(Users.stars, Users.level).where(Users.tg_id == tg_id)) добавь старс и левел в параметры
        #for tupl in info:
            #for t1 in tupl:
                #listt.append(t1)
        await session.execute(update(Users).where(Users.tg_id == tg_id).values(stars = str(int(stars)+ rightans), level = str(float(level) + rightans/100), questionlevel=str(questionlevel), questiontime = questiontime))
        await session.commit()

async def update_questiontime(questiontime, tg_id):
    async with async_session() as session:
        await session.execute(update(Users).where(Users.tg_id == tg_id).values(questiontime = questiontime))
        await session.commit()

#User registration----------------------------------------------------------------------------------------------------        
async def add_user(p):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == p))
        if not user:
            session.add(User(tg_id= p))
            await session.commit()
            return True
        else:       
            return False
        
async def check_user(tg_id, tg_username):
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id == tg_id-1))
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
        return f"Stars: {str(listt[0])}\nLevel: {str(listt[1])[:-2]} | {str(listt[1])[-2:]}%" # тут ошибка индекса
             
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


async def retrieve_stars_level_tasklevel_tasktime(tg_id, task_level, task_time):
    async with async_session() as session:
        listt = []
        questionlevel = await session.execute(select(Users.stars, Users.level, task_level, task_time).where(Users.tg_id == tg_id))
        for tupl in questionlevel:
            for t1 in tupl:
                listt.append(t1)
        return listt    

async def update_wordstime(wordstime, tg_id):
    async with async_session() as session:
        await session.execute(update(Users).where(Users.tg_id == tg_id).values(wordstime = wordstime))
        await session.commit()
########################################################################################################################################################################################
async def db_helper(tg_id, task_param = 'questiontime', command= None, stars = 0, level = 0, task_level = 0): #stars, level, wordslevel, wordstime, rightans,  tg_id
    #instance = await session.get(Users, id) <app.database.models.Users object at 0x000001E98C6D7940>
    async with async_session() as session: 
        info = await session.execute(select(Users).where(Users.tg_id == tg_id)) 
        db_string = info.scalars().first()
        level_time = getattr(db_string, task_param)
        if command: # старт задания на команду
            if db_string.is_subscribed: # если подписан, новые задания без ограничений
                return level_time[:-9]
            else:
                if datetime.datetime.now().strftime("%x") == level_time[-8:]:
                    return False
                setattr(db_string, task_param, level_time[:-8] + datetime.datetime.now().strftime("%x")) # повторно команда сработает через день 
                await session.commit()
                return level_time[:-9]  
        else:     
            setattr(db_string, task_param, str(int(level_time[:-9]) + task_level) + level_time[-9:]) # запись старс левел и уровня таска, функция без команды
            db_string.stars += stars
            db_string.level += level
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
