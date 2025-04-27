from app.database.models import async_session, engine
from app.database.models import User, Uncountable, Preposition, Words, Users, Question
from sqlalchemy import select, update, delete, func
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random
from aiogram.filters.callback_data import CallbackData

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
# PREP
async def randforsentense(tableparam):
    async with async_session() as session:
        max = await session.scalar(select(func.max(tableparam)))
        rand = random.randint(1, max)
        return rand
    
async def not_randforsentense(id):
    async with async_session() as session:
        preplevel = await session.scalar(select(Users.preplevel).where(Users.tg_id == id))
        if preplevel == 0:
            number = 1
        else:
            number = preplevel * 10 + 1    
        return number    

# PREP
async def retrieve_sentense(rand):
    async with async_session() as session:
        listt = []
        sentense = await session.execute(select(Preposition.part1, Preposition.part2).where(Preposition.id == rand)) 
        for tupl in sentense:
            for t1 in tupl:
                listt.append(t1)
        return f"{listt[0]}   ...   {listt[1]}"
    
# TRANSLATION
async def retrieve_word(column, rand):
    async with async_session() as session:
        word = await session.scalar(select(column).where(Words.id == rand))
        return word.split(', ')

    

class MyCallback(CallbackData, prefix="myy"):
    b: str
    r: int
    rightans: int
    counter: int
    exit: str
    
    


class MyCallback3(CallbackData, prefix="myyy"):
    r: int
    rightans: int
    counter: int
       

class MyCallback2(CallbackData, prefix="my"):
    word: str
    keyboard: str     
   
async def inlinebuttonss(rand, right= 0, counter= 0):
    async with async_session() as session:
        keyboard = InlineKeyboardBuilder()
        prep = await session.scalar(select(Preposition.prep).where(Preposition.id == rand))
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
            keyboard.add(InlineKeyboardButton(text = button, callback_data= MyCallback(b= button, r= rand, rightans= right, counter= counter, exit = '').pack()))          
        return keyboard.adjust(3).as_markup()     #adjust(2)    





async def inlinebuttons(n):
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
                keyboard.add(InlineKeyboardButton(text = button, callback_data= MyCallback2(word= button, keyboard= x).pack()))          
        return keyboard.adjust(3).as_markup()     #adjust(2)    

async def inlinebuttons2(list):
        x = ','.join(list)
        keyboard = InlineKeyboardBuilder()
        for button in list:     
                keyboard.add(InlineKeyboardButton(text = button, callback_data= MyCallback2(word= button, keyboard= x).pack()))          
        return keyboard.adjust(3).as_markup()     #adjust(2)    
        

async def add_user(p):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == p))
        if not user:
            session.add(User(tg_id= p))
            await session.commit()
            return True
        else:
            return False
        
async def check_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id == tg_id))
        if not user:
            session.add(Users(tg_id = tg_id))
            await session.commit()
            return False
        else:
            return True    
        

async def retrieve_rate(id):
    async with async_session() as session:
        listt = []
        sentense = await session.execute(select(Users.stars, Users.level).where(Users.tg_id == id)) 
        for tupl in sentense:
            for t1 in tupl:
                listt.append(t1)
        return f"Stars: {listt[0]}\nLevel: {listt[1]}"   


async def retrieve_stars(id):
    async with async_session() as session:
        stars = await session.scalar(select(Users.stars).where(Users.tg_id == id))
        return stars    

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





async def write_words(word, translation):
    async with async_session() as session:
        session.add(Uncountable(word = word, translation = translation))
        await session.commit()

async def delete_table():
    async with async_session() as session:
        session.delete()
        await session.commit()

