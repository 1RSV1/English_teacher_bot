from sqlalchemy import BigInteger, String, ForeignKey, create_engine, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import datetime
from sqlalchemy.sql import func
from aiogram.filters.callback_data import CallbackData

engine = create_async_engine(url= "")

async_session = async_sessionmaker(engine)

engine2 = create_async_engine(url= "sqlite+aiosqlite:///db.sqlite3")

async_session2 = async_sessionmaker(engine2)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users" # node js uses!

    id: Mapped[int] = mapped_column(primary_key= True)
    tg_id: Mapped[BigInteger] = mapped_column(BigInteger)
    tg_username: Mapped[str] = mapped_column(String(125))
    stars: Mapped[int] = mapped_column(default = 0)
    level: Mapped[float] = mapped_column(default = 0.00) 
    streak: Mapped[int] = mapped_column(default = 1) # дефолт 1 тк нет обновления дня в первый день по дате 
    test_level_time: Mapped[str] = mapped_column(default = '1 00/00/00')
    present_level_time: Mapped[str] = mapped_column(default = '1 0 00/00/00')
    past_level_time: Mapped[str] = mapped_column(default = '1 0 00/00/00')
    future_level_time: Mapped[str] = mapped_column(default = '1 0 00/00/00')
    prep_level_time: Mapped[str] = mapped_column(default = '0') 
    question_level_time: Mapped[str] = mapped_column(default = '1 00/00/00')
    words_level_time: Mapped[str] = mapped_column(default = '0')
    quiz_level_time: Mapped[str] = mapped_column(default = '1 00/00/00')
    listening_level_time: Mapped[str] = mapped_column(default = '1 00/00/00')
    speaking_level_time: Mapped[str] = mapped_column(default = '1 0 00/00/00')
    is_subscribed: Mapped[bool] = mapped_column(default = False)
    createdAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now())


class Present_Past(Base): # test
    __tablename__ = "present_and_past"

    id: Mapped[int] = mapped_column(primary_key= True)
    sentence: Mapped[str] = mapped_column(String(125), nullable= True)
    p1: Mapped[str] = mapped_column(String(125), nullable= True)
    p2: Mapped[str] = mapped_column(String(125), nullable= True)
    p3: Mapped[str] = mapped_column(String(125), nullable= True)
    p4: Mapped[str] = mapped_column(String(125), nullable= True)
    p5: Mapped[str] = mapped_column(String(125), nullable= True)

class Listening(Base): 
    __tablename__ = "listening"

    id: Mapped[int] = mapped_column(primary_key= True)
    p1: Mapped[str] = mapped_column(String(125), nullable= True)
    p2: Mapped[str] = mapped_column(String(125), nullable= True)
    p3: Mapped[str] = mapped_column(String(125), nullable= True)
    
class Speaking(Base): 
    __tablename__ = "speaking"

    id: Mapped[int] = mapped_column(primary_key= True)
    sentence: Mapped[str] = mapped_column(String(125), nullable= True)
    

class Present_Past_Compile(Base): 
    __tablename__ = "present_and_past_compile"

    id: Mapped[int] = mapped_column(primary_key= True)
    p1: Mapped[str] = mapped_column(String(125), nullable= True)
    p2: Mapped[str] = mapped_column(String(125), nullable= True)
    p3: Mapped[str] = mapped_column(String(125), nullable= True)
    p4: Mapped[str] = mapped_column(String(125), nullable= True)
    p5: Mapped[str] = mapped_column(String(125), nullable= True)
    p6: Mapped[str] = mapped_column(String(125), nullable= True)
    p7: Mapped[str] = mapped_column(String(125), nullable= True)
    p8: Mapped[str] = mapped_column(String(125), nullable= True)
    p9: Mapped[str] = mapped_column(String(125), nullable= True)
    p10: Mapped[str] = mapped_column(String(125), nullable= True)

class Present_Past_Quiz(Base):
    __tablename__ = "present_and_past_quiz"

    id: Mapped[int] = mapped_column(primary_key= True, autoincrement= True)
    question: Mapped[str] = mapped_column(String(125), nullable= True)
    open_period: Mapped[int] = mapped_column(nullable= True)
    option1: Mapped[str] = mapped_column(String(125), nullable= True)
    option2: Mapped[str] = mapped_column(String(125), nullable= True)
    option3: Mapped[str] = mapped_column(String(125), nullable= True)
    option4: Mapped[str] = mapped_column(String(125), nullable= True)
    option5: Mapped[str] = mapped_column(String(125), nullable= True)
    explanation: Mapped[str] = mapped_column(String(125), nullable= True)

class Present_Past_Regular(Base):
    __tablename__ = "present_and_past_regulars"

    id: Mapped[int] = mapped_column(primary_key= True, autoincrement= True)
    question: Mapped[str] = mapped_column(String(125), nullable= True)
    open_period: Mapped[int] = mapped_column(default = 0)
    option1: Mapped[str] = mapped_column(String(125), nullable= True)
    option2: Mapped[str] = mapped_column(String(125), nullable= True)
    option3: Mapped[str] = mapped_column(String(125), nullable= True)
    option4: Mapped[str] = mapped_column(String(125), nullable= True)
    option5: Mapped[str] = mapped_column(String(125), nullable= True)
    option6: Mapped[str] = mapped_column(String(125), nullable= True)
    option7: Mapped[str] = mapped_column(String(125), nullable= True)
    option8: Mapped[str] = mapped_column(String(125), nullable= True) 
    right_options: Mapped[str] = mapped_column(String(125), nullable= True)
    explanation: Mapped[str] = mapped_column(String(125), nullable= True)        

class Test2(Base): # test
    __tablename__ = "test2"

    id: Mapped[int] = mapped_column(primary_key= True)
    sentence: Mapped[str] = mapped_column(String(125), nullable= True)
    p1: Mapped[str] = mapped_column(String(125), nullable= True)
    p2: Mapped[str] = mapped_column(String(125), nullable= True)
    p3: Mapped[str] = mapped_column(String(125), nullable= True)
    p4: Mapped[str] = mapped_column(String(125), nullable= True)
    p5: Mapped[str] = mapped_column(String(125), nullable= True)
    

class Test(Base): #words
    __tablename__ = "test"

    id: Mapped[int] = mapped_column(primary_key= True)
    p1: Mapped[str] = mapped_column(String(125), nullable= True)
    p2: Mapped[str] = mapped_column(String(125), nullable= True)
    p3: Mapped[str] = mapped_column(String(125), nullable= True)
    p4: Mapped[str] = mapped_column(String(125), nullable= True)
    p5: Mapped[str] = mapped_column(String(125), nullable= True)
    p6: Mapped[str] = mapped_column(String(125), nullable= True)
    p7: Mapped[str] = mapped_column(String(125), nullable= True)
    p8: Mapped[str] = mapped_column(String(125), nullable= True)
    p9: Mapped[str] = mapped_column(String(125), nullable= True)
    p10: Mapped[str] = mapped_column(String(125), nullable= True)


'''
class Post(Base):
    # разобраться
    author: Mapped['User'] = relationship(back_populates='posts')
'''


class Polls(Base):
    __tablename__ = "polls"

    id: Mapped[int] = mapped_column(primary_key= True, autoincrement= True)
    question: Mapped[str] = mapped_column(String(125), nullable= True)
    open_period: Mapped[str] = mapped_column(String(125), nullable= True)
    option1: Mapped[str] = mapped_column(String(125), nullable= True)
    option2: Mapped[str] = mapped_column(String(125), nullable= True)
    option3: Mapped[str] = mapped_column(String(125), nullable= True)
    option4: Mapped[str] = mapped_column(String(125), nullable= True)
    option5: Mapped[str] = mapped_column(String(125), nullable= True)
    option6: Mapped[str] = mapped_column(String(125), nullable= True)
    option7: Mapped[str] = mapped_column(String(125), nullable= True)
    option8: Mapped[str] = mapped_column(String(125), nullable= True)
    option9: Mapped[str] = mapped_column(String(125), nullable= True)
    option10: Mapped[str] = mapped_column(String(125), nullable= True)
    explanation: Mapped[str] = mapped_column(String(125), nullable= True)

class Quizes(Base):
    __tablename__ = "quizes"

    id: Mapped[int] = mapped_column(primary_key= True, autoincrement= True)
    question: Mapped[str] = mapped_column(String(125), nullable= True)
    open_period: Mapped[str] = mapped_column(String(125), nullable= True)
    option1: Mapped[str] = mapped_column(String(125), nullable= True)
    option2: Mapped[str] = mapped_column(String(125), nullable= True)
    option3: Mapped[str] = mapped_column(String(125), nullable= True)
    option4: Mapped[str] = mapped_column(String(125), nullable= True)
    option5: Mapped[str] = mapped_column(String(125), nullable= True)
    explanation: Mapped[str] = mapped_column(String(125), nullable= True)

class Regular(Base):
    __tablename__ = "regulars"

    id: Mapped[int] = mapped_column(primary_key= True, autoincrement= True)
    question: Mapped[str] = mapped_column(String(125), nullable= True)
    open_period: Mapped[int] = mapped_column(default = 0)
    option1: Mapped[str] = mapped_column(String(125), nullable= True)
    option2: Mapped[str] = mapped_column(String(125), nullable= True)
    option3: Mapped[str] = mapped_column(String(125), nullable= True)
    option4: Mapped[str] = mapped_column(String(125), nullable= True)
    option5: Mapped[str] = mapped_column(String(125), nullable= True)
    option6: Mapped[str] = mapped_column(String(125), nullable= True)
    option7: Mapped[str] = mapped_column(String(125), nullable= True)
    option8: Mapped[str] = mapped_column(String(125), nullable= True) 
    right_options: Mapped[str] = mapped_column(String(125), nullable= True)
    explanation: Mapped[str] = mapped_column(String(125), nullable= True)    

class Preposition(Base):
    __tablename__ = "prepositionss"

    id: Mapped[int] = mapped_column(primary_key= True, autoincrement= True)
    sentence: Mapped[str] = mapped_column(String(125), nullable= True)
    p1: Mapped[str] = mapped_column(String(125), nullable= True)
    p2: Mapped[str] = mapped_column(String(125), nullable= True)
    p3: Mapped[str] = mapped_column(String(125), nullable= True)
    p4: Mapped[str] = mapped_column(String(125), nullable= True)
    p5: Mapped[str] = mapped_column(String(125), nullable= True)



      

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
