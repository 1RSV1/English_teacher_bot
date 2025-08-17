from aiogram import F, Router, Bot
from aiogram.filters.command import Command, CommandStart
from aiogram.types import Message, CallbackQuery, ForceReply, LabeledPrice, PreCheckoutQuery, input_poll_option, PollAnswer, Poll, MessageEntity, User, FSInputFile, ForceReply
import app.keyboards as kb
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.middlewares import PollAnswerMiddle, PollMiddle, MessageMiddle # импорт мидлвари
import app.database.requests as rq
from app.database.requests import  Questions, MyCallback3, Variable, Variable2, Payment, Conditionals, Control
from app.database.models import async_session, Preposition, Test2, Test,  Quizes, Regular, Present_Past, Present_Past_Quiz, Present_Past_Regular, Present_Past_Compile, Listening, Speaking
from sqlalchemy import select, func
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.fsm.storage.redis import RedisStorage
import os, time, json, string, datetime, random, sys
from aiogram import flags
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment
from gtts import gTTS
import re
import subprocess
import tiktoken


load_dotenv()   
bot = Bot(token=os.getenv('TOKEN'))
router = Router()
router.message.middleware(MessageMiddle())
#router.callback_query.middleware(Test())
router.poll_answer.middleware(MessageMiddle())
router.poll.middleware(PollMiddle())
router.message.middleware(ChatActionMiddleware())
from gtts import gTTS


#get_prober_name = lambda: r'C:\Users\v.erasov\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1.1-full_build\bin\ffprobe.exe'


class SomeClass(StatesGroup): # FSM
    translation = State()
    number = State()
    uncountable = State()
    word = State()
    trans = State()
    list = State()
    voice = State()


client = OpenAI(
    #base_url="https://api.deepseek.com",
    api_key = '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'
    )    



storage = RedisStorage.from_url('redis://default:%2CE%3FYhUP7rq%2C%5C54@147.45.106.233:6379')

@router.message(CommandStart())
async def cmd_start(message: Message):
    if await rq.check_user(message.from_user.id, message.from_user.username):
        await message.answer('Твои статы:' + '\n' + await rq.retrieve_rate(message.from_user.id)) #'. Это бот для изучения английского языка. Выполняй задания, соревнуйся с другими участниками, отслеживай свой прогресс с помощью тестов'
    else:
        await message.answer('Привет, ' + message.from_user.first_name  + '\n' +  '\n' + await rq.retrieve_rate(message.from_user.id))

@router.message(Command('present_and_past'))
async def cmd_present(message: Message):
    task_level = await rq.db_helper(message.from_user.id, task_param = 'present_level_time', command= 'present_level_time')
    if task_level:
        if task_level[-4:-3] != '':
            if int(task_level[-4:-3]) == 2 and int(task_level[-1]) == 0:
                level = int(task_level[:-4])*3
                await message.answer('Выбери пары из левой и правой колонки по смыслу', reply_markup= await rq.test('pr', Present_Past_Compile, level + 1, storage = storage))
            #await message.answer(' ?', reply_markup= await rq.collect_words(id = 1, table = Question, storage = storage)) CONDITIONALS
            elif int(task_level[-4:-3]) == 5 and int(task_level[-1]) == 1:
                await rq.retrieve_three_regulars(Present_Past_Regular , int(task_level[:-4])*3 + 1, message.from_user.id, storage = storage, bot = bot)
                #await message.answer(' ?', reply_markup= await rq.collect_words(id = 1, table = Question, storage = storage)) REGULARS
            elif int(task_level[-4:-3]) == 9 and int(task_level[-1]) == 2:
                await rq.retrieve_three_quizes(Present_Past_Quiz, int(task_level[:-4])*3 + 1, message.from_user.id, storage = storage, bot = bot)
                #await message.answer(' ?', reply_markup= await rq.collect_words(id = 1, table = Question, storage = storage)) QUIZ
            else: 
                await message.answer(text= await rq.three_options_sentence(int(task_level[:-2]), Present_Past), reply_markup= await rq.three_options_keyboard('pr', int(task_level[:-2]), Present_Past))   
        else: 
                await message.answer(text= await rq.three_options_sentence(int(task_level[:-2]), Present_Past), reply_markup= await rq.three_options_keyboard('pr', int(task_level[:-2]), Present_Past))                    
    else:
        await message.answer('Сегодня ты уже прошел тест. Новый появится завтра') #reply_markup= await kb.two_options(data[2], 'questions'

@router.message(Command('past'))
async def cmd_present(message: Message):
    task_level = await rq.db_helper(message.from_user.id, task_param = 'past_level_time', command= 'past_level_time')
    if task_level:
        if int(task_level[-4:-3]) == 2 and int(task_level[-1]) == 0:
            await message.answer('Выбери пары из левой и правой колонки по смыслу', reply_markup= await rq.test(Test, int(task_level[:-4])*5 + 1))
            #await message.answer(' ?', reply_markup= await rq.collect_words(id = 1, table = Question, storage = storage)) CONDITIONALS
        elif int(task_level[-4:-3]) == 5 and int(task_level[-1]) == 1:
            await rq.retrieve_three_regulars(Regular , int(task_level[:-4])*3 + 1, message.from_user.id, storage = storage, bot = bot)
            #await message.answer(' ?', reply_markup= await rq.collect_words(id = 1, table = Question, storage = storage)) REGULARS
        elif int(task_level[-4:-3]) == 9 and int(task_level[-1]) == 2:
            await rq.retrieve_three_quizes(Quizes , int(task_level[:-4])*3 + 1, message.from_user.id, storage = storage, bot = bot)
            #await message.answer(' ?', reply_markup= await rq.collect_words(id = 1, table = Question, storage = storage)) QUIZ
        else: 
            await message.answer(text= await rq.three_options_sentence(int(task_level), Test2), reply_markup= await rq.three_options_keyboard('t', int(task_level), Test2))               
    else:
        await message.answer('Сегодня ты уже прошел тест. Новый появится завтра') #reply_markup= await kb.two_options(data[2], 'questions'

@router.message(Command('future'))
async def cmd_present(message: Message):
    task_level = await rq.db_helper(message.from_user.id, task_param = 'past_level_time', command= 'past_level_time')
    if task_level:
        if int(task_level[-4:-3]) == 2 and int(task_level[-1]) == 0:
            await message.answer('Выбери пары из левой и правой колонки по смыслу', reply_markup= await rq.test(Test, int(task_level[:-4])*5 + 1))
            #await message.answer(' ?', reply_markup= await rq.collect_words(id = 1, table = Question, storage = storage)) CONDITIONALS
        elif int(task_level[-4:-3]) == 5 and int(task_level[-1]) == 1:
            await rq.retrieve_three_regulars(Regular , int(task_level[:-4])*3 + 1, message.from_user.id, storage = storage, bot = bot)
            #await message.answer(' ?', reply_markup= await rq.collect_words(id = 1, table = Question, storage = storage)) REGULARS
        elif int(task_level[-4:-3]) == 9 and int(task_level[-1]) == 2:
            await rq.retrieve_three_quizes(Quizes , int(task_level[:-4])*3 + 1, message.from_user.id, storage = storage, bot = bot)
            #await message.answer(' ?', reply_markup= await rq.collect_words(id = 1, table = Question, storage = storage)) QUIZ
        else: 
            await message.answer(text= await rq.three_options_sentence(int(task_level), Test2), reply_markup= await rq.three_options_keyboard('t', int(task_level), Test2))               
    else:
        await message.answer('Сегодня ты уже прошел тест. Новый появится завтра') #reply_markup= await kb.two_options(data[2], 'questions'

@router.message(Command('listening')) # lambda message: message.voice is not None
async def cmd_listening(message: Message):
    task_level = 1 #await rq.db_helper(message.from_user.id, task_param = 'listening_level_time', command= 'listening_level_time')
    if task_level:
        voice = FSInputFile(f'listening/{task_level}.opus', filename = 'gg')
        await message.answer_voice(voice = voice, protect_content = True, reply_markup= await rq.three_options_keyboard('l', int(task_level), Listening))

@router.callback_query(Control.filter(F.mark == 'l'))
async def my_callback(query: CallbackQuery, callback_data: Control):
    for list in query.message.reply_markup.inline_keyboard:
        if list[0].callback_data[-3] == '0':
            caption = list[0].text
            break
    await query.message.edit_caption(caption = caption, reply_markup = None)
    if callback_data.ans == '0': # нулевой индекс всегда правильный ответ(лист перемешан)
        callback_data.rightans += 1
        await query.answer("✅✅✅")
    else:
        await query.answer("❌❌❌")

    if callback_data.id%3 == 0:
        await rq.db_helper(query.from_user.id, task_param = 'listening_level_time', stars = int(callback_data.rightans), level = round(callback_data.rightans/100, 2), task_level = str(3) + ' 0')
        await query.message.answer(text=f'Тест пройден. Здесь анализ ответов исходя из  {callback_data.rightans}') # написать функцию
    else:   
        voice = FSInputFile(f'listening/{callback_data.id + 1}.opus', filename = 'gg') 
        await query.message.answer_voice(voice = voice, reply_markup= await rq.three_options_keyboard('l', callback_data.id + 1, Listening, callback_data.rightans))        


@router.message(Command('speaking')) # lambda message: message.voice is not None
async def handle_voice_state(message: Message, state: FSMContext):
    task_level = await rq.db_helper(message.from_user.id, task_param = 'speaking_level_time', command= 'speaking_level_time')
    if task_level:
        sentences = await rq.retrieve_three_ai_sentences(Speaking, int(task_level[:-2]))
        await state.update_data(first = sentences[0])
        await state.update_data(second = sentences[1])
        await state.update_data(third = sentences[2])
        await state.update_data(current = 'first')
        answer = await message.answer(text= f'Repeat after me: \n\n *{sentences[0]}*', parse_mode = 'MarkdownV2')
        await state.update_data(message_id = answer.message_id)
        await state.set_state(SomeClass.voice)


@router.message(SomeClass.voice) # СОСТОЯНИЯ ВЫНОСИМ ВПЕРЕД ДЛЯ ИСКЛЮЧЕНИЯ СРАБАТЫВАНИЯ КОМАНД В ОТКРЫТОМ СОСТОЯНИИ
async def handle_voice_state(message: Message, state: FSMContext):
    
    if message.voice is None:
        await state.clear()
        await message.answer(text = 'You opened a lesson of speaking . Send a voice message next time .')
        return
    
    #try:            
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
    print(transcription)
    data = await state.get_data()
    if transcription[:-2].casefold() == data[data['current']].casefold()[:-1] if data[data['current']].endswith('?') else data[data['current']].casefold():
        await bot.edit_message_text(chat_id = message.from_user.id, message_id = data['message_id'], text = "✅✅✅") # по айди из состояния 
    else:
        await bot.edit_message_text(chat_id = message.from_user.id, message_id = data['message_id'], text = f"❌❌❌\n\n{data[data['current']]}\n\nYou said: *{transcription[:-2] if transcription[:-2] == '.' else transcription[:-1]}*", parse_mode = 'MarkdownV2') # по айди из состояния и новое сообщение отправляем
    
    await state.set_state(SomeClass.voice)
    if data['second']:
        data['current'] = 'second'
        answer = await message.answer(text= f'Repeat after me: \n\n *{data["second"]}*', parse_mode = 'MarkdownV2')
        await state.update_data(message_id = answer.message_id)
        await state.update_data(second = 0)
    elif data['third']:
        data['current'] = 'third'
        answer = await message.answer(text= f'Repeat after me: \n\n *{data["third"]}*', parse_mode = 'MarkdownV2')
        await state.update_data(message_id = answer.message_id)
        await state.update_data(third = 0)
    else:
        await message.answer(text='тест закончился, состояние зачищено')
        await state.clear()
    #except:
        await state.clear()
        await message.answer(text = 'Something went wrong .')
        




#@router.message(lambda message: message.text is not None)
#async def handle_all_messages(message: Message):
    #await message.answer(text = f'*{message.text}* ~{message.text}~', parse_mode = 'MarkdownV2')
encoder = tiktoken.encoding_for_model("gpt-4-turbo")

def count_tokens(text):
    return len(encoder.encode(text))



assistant = client.beta.assistants.create(
    name="English teacher",
    instructions="You are a friendly and professional English teacher. Your name is Kate. You pretend that you can hear what users tell you" \
    "Your responses should be brief, concise, and pedagogically helpful (2-3 sentences max). " \
    "Focus on clear explanations with simple examples when needed. Never correct user's mistakes. " \
    "Encourage learning by asking auxiliary questions at the end of the answer.",
    model="gpt-4-turbo"
)   
ASSISTANT_ID = assistant.id
@router.message(lambda message: message.voice is not None or message.text is not None , flags={'chat_action': 'record_voice', 'rate_limit': {'rate': 5}}) # lambda message: message.voice is not None
async def handle_all_audios(message: Message):
    if message.from_user.id in [486982133, 155269575]:
        pass
    else:
        await message.answer('доступ закрыт')
    #await storage.redis.delete(message.from_user.id)
    thread = await storage.redis.get(name = message.from_user.id) 
    print(thread) 
    if not thread:
         thread = client.beta.threads.create()
         obj = json.dumps(thread.id)
         await storage.redis.set(name = message.from_user.id, value = obj)
         thread_id = thread.id
         
    else:
        thread_id = await storage.redis.get(name = message.from_user.id) 
        thread_id = json.loads(thread_id)
    
    if message.voice is not None:    
        await bot.download(message.voice.file_id, f'audio/{message.from_user.id}.mp3')
          
        #model = 'whisper-1'
        subprocess.run([
            'ffmpeg',
            '-y',
            '-loglevel', 
            'error',
            '-i',
            f'audio/{message.from_user.id}.mp3',
            '-af',
            'areverse,silenceremove=start_periods=1:start_duration=0.05:start_silence=0.1:start_threshold=0.02,areverse,silenceremove=start_periods=1:start_duration=0.05:start_silence=0.1:start_threshold=0.02',
            f'audio/{message.from_user.id}-trim.mp3'
        ])
        try:
            transcription = client.audio.transcriptions.create(
                    model= 'whisper-1',
                    file= open(f'audio/{message.from_user.id}-trim.mp3', "rb"),
                    response_format="text"  # or "json", "srt", "verbose_json", "vtt"
                    )
            #duration = transcription.duration # voice in seconds
        except Exception as e:
            transcription = f'sorry, i dont hear you {e}'
            await message.answer(transcription)
            return
    else:
        transcription = message.text  

    spelling = [{"role": "system", "content": f"Correct spelling. Choose only one of three options for every sentence: 1. If a sentence only has a wrong sentence structure wrap the whole sentence in '~' and add a corrected sentence wrapped in '*' right after the sentence. 2. If the word order is correct but some words are grammatically wrong, wrap these words in '~' and add a correct words wrapped in '*' right after every wrong word. 3. If the sentence has no mistakes leave the sentence without changing"}, {'role': 'user', 'content': transcription}]       
    
    spelling_response = client.chat.completions.create(model = 'gpt-4.1-nano', messages = spelling)
    input_tokens_spelling = spelling_response.usage.prompt_tokens
    output_tokens_spelling = spelling_response.usage.completion_tokens
    total_tokens_spelling = spelling_response.usage.total_tokens
    corrected = spelling_response.choices[0].message.content
    corrected2 = ''
    if '*' not in corrected and '~' not in corrected:
            corrected2 = '✅*Correct\!*'
    else:        
        for letter in corrected:
            
            if letter in ['.', '!', '?']:
                corrected2 += '\\'+ letter
            else:
                corrected2 += letter  
    print(corrected2)
    try:               
        await message.answer(text = corrected2, parse_mode = 'MarkdownV2') 
    except Exception as e:
        await message.answer(text = f'{e}')

    
    
    client.beta.threads.messages.create(
        thread_id= thread_id,
        role="user",
        content= transcription
    )    

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break

    messages = client.beta.threads.messages.list(thread_id=thread_id)

    input_tokens = 0
    output_tokens = 0

    for msg in messages.data:
        print(msg.content[0].text.value)
        if msg.role == "system":
            input_tokens += count_tokens(msg.content[0].text.value)
        if msg.role == "user":
            input_tokens += count_tokens(msg.content[0].text.value)
        elif msg.role == "assistant":
            output_tokens += count_tokens(msg.content[0].text.value)

    assistant_response = messages.data[0].content[0].text.value

    tts = gTTS(text= assistant_response, lang="en", tld='co.za')
    tts.save(f'audio/{message.from_user.id}.mp3') # сохраняет только в mp3
    
    audio = AudioSegment.from_mp3(f'audio/{message.from_user.id}.mp3') # install ffmpeg on ubuntu
    audio.export(f'audio/{message.from_user.id}.opus', format='opus', codec="libopus", bitrate="64k")   
    voice = FSInputFile(f'audio/{message.from_user.id}.opus', filename = 'gg')  
    await bot.send_voice(chat_id = message.from_user.id, voice = voice)
    if message.from_user.id == 486982133:   
        if message.voice is not None:
            await bot.send_voice(chat_id = 155269575, voice = message.voice.file_id)
        else:
            await bot.send_message(chat_id=155269575, text= message.text) 
        await bot.send_voice(chat_id = 155269575, voice = voice) 
    if message.from_user.id == 155269575:       
        await message.answer(f'Вход орфография: {input_tokens_spelling} \n\n Выход орфография: {output_tokens_spelling} \n\n Всего орфография: {total_tokens_spelling} \n\n\n Вход тред: {input_tokens}\n\n Выход тред: {output_tokens}\n\n')

    



#model = whisper.load_model("small")
@router.message(lambda message: message.voice is not None or message.text is not None , flags={'chat_action': 'record_voice', 'rate_limit': {'rate': 5}}) # lambda message: message.voice is not None
async def handle_all_audios(message: Message):
    value = await storage.redis.get(name = message.from_user.id)    
    if not value:
         await storage.redis.set(name = message.from_user.id, value = '[]', ex = 60)
         value = []
    else:
        value =  json.loads(value)    
    if message.voice is not None:    
        await bot.download(message.voice.file_id, f'audio/{message.from_user.id}.mp3')
        print(value)  
        #model = 'whisper-1'
        subprocess.run([
            'ffmpeg',
            '-y',
            '-loglevel', 
            'error',
            '-i',
            f'audio/{message.from_user.id}.mp3',
            '-af',
            'areverse,silenceremove=start_periods=1:start_duration=0.05:start_silence=0.1:start_threshold=0.02,areverse,silenceremove=start_periods=1:start_duration=0.05:start_silence=0.1:start_threshold=0.02',
            f'audio/{message.from_user.id}-trim.mp3'
        ])
        try:
            transcription = client.audio.transcriptions.create(
                    model= 'whisper-1',
                    file= open(f'audio/{message.from_user.id}-trim.mp3', "rb"),
                    response_format="text"  # or "json", "srt", "verbose_json", "vtt"
                    )
        except:
            transcription = 'sorry, i dont hear you'
            await message.answer(transcription)
            return
    else:
        transcription = message.text    
    #result = model.transcribe(f'audio/{message.from_user.id}.mp3', fp16=False)
    #transcription = result["text"]
    print(transcription) 
    spelling = [{"role": "system", "content": f"Correct spelling.  If a sentence has a mistake, wrap the mistake in '~' and add a correction wrapped in '*' right after the mistake. Return 'Correct!' if there are no corrections"}, {'role': 'user', 'content': transcription}]       
    name = ['Vad']
    data = [{"role": "system", "content": f"You are a friendly and professional English teacher. If the response requires the information about the user try to find it in  {value} object. Your responses should be brief, concise, and pedagogically helpful (1-2 sentences max). Focus on clear explanations with simple examples when needed. Correct mistakes gently and encourage learning."}, {'role': 'user', 'content': transcription}]
    spelling_response = client.chat.completions.create(model = 'gpt-4.1-nano', messages = spelling)
    response = client.chat.completions.create(model = 'gpt-4.1-nano', messages = data)
    corrected = spelling_response.choices[0].message.content
    corrected2 = ''
    for letter in corrected:
        if letter in ['.', '!', '?']:
             corrected2 += '\\'+ letter
        else:
             corrected2 += letter     
    await message.answer(text = corrected2, parse_mode = 'MarkdownV2') 
    text_gpt = response.choices[0].message.content 
    print(text_gpt)
    value.append((transcription, text_gpt))
    value =  json.dumps(value)
    await storage.redis.set(name = message.from_user.id, value = value, ex = 60)
    '''
    matches = re.findall(r'\{([^{}]+)\}', text_gpt)
    if matches:
        name += matches
    if text_gpt[0] in string.ascii_letters:
        lang = 'en'
    else:
        lang = 'ru'   
    '''
    tts = gTTS(text= text_gpt, lang="en")
    tts.save(f'audio/{message.from_user.id}.mp3') # сохраняет только в mp3
    
    audio = AudioSegment.from_mp3(f'audio/{message.from_user.id}.mp3') # install ffmpeg on ubuntu
    audio.export(f'audio/{message.from_user.id}.opus', format='opus', codec="libopus", bitrate="64k")   
    voice = FSInputFile(f'audio/{message.from_user.id}.opus', filename = 'gg')
    await bot.send_voice(chat_id = message.from_user.id, voice = voice) 
    
    




@router.message(Command('quiz'), flags={'chat_action': 'typing', 'rate_limit': {'rate': 5}})
@flags.chat_action(initial_sleep=0, action="typing", interval=3)
async def cmd_poll(message: Message):
    await rq.retrieve_three_quizes(Quizes ,1, message.from_user.id, storage = storage, bot = bot)
    
    
    

@router.poll()
async def poll_answer_handler(poll: Poll):
    try:
        d = await storage.redis.get(name = str(poll.explanation_entities[0].user.id) + '_quiz')
        d = json.loads(d.decode())

        voter_count = 0
        for i in range(len(poll.options)):
            if poll.options[i].voter_count:
                voter_count += poll.options[i].voter_count
            if poll.options[i].voter_count == 1 and i == poll.correct_option_id:
                d['ans'] += 1
        if  voter_count > 1:
                return   
            
        if d['second']:
            option1 = d['second']['option1']
            options = []
            for x, y in d['second'].items():
                if x.startswith('option') and y:
                    options.append(input_poll_option.InputPollOption(text= d['second'][x]))
            random.shuffle(options)        
            await bot.send_poll( 
                                chat_id = poll.explanation_entities[0].user.id,
                                question= d['second']['question'], 
                                open_period = int(d['second']['open_period']), # переделать в цифру в бд
                                options= options, 
                                correct_option_id= options.index(input_poll_option.InputPollOption(text = option1)),
                                type = 'quiz',
                                explanation = d['second']['explanation'], 
                                explanation_entities = [MessageEntity(type = 'text_mention', offset = 0, length = len(d['second']['explanation']), user = User(id = poll.explanation_entities[0].user.id, is_bot = False, first_name = 'vad'))]                        
                                )
            d['second'] = 0
            await storage.redis.set(name = str(poll.explanation_entities[0].user.id)+ '_quiz', value = json.dumps(d), ex = 60)
        
        elif d['third']:
            option1 = d['third']['option1']
            options = []
            for x, y in d['third'].items():
                if x.startswith('option') and y:
                    options.append(input_poll_option.InputPollOption(text= d['third'][x]))
            random.shuffle(options)        
            await bot.send_poll( 
                                chat_id = poll.explanation_entities[0].user.id,
                                question= d['third']['question'], 
                                open_period = int(d['third']['open_period']), # переделать в цифру в бд
                                options= options, 
                                correct_option_id= options.index(input_poll_option.InputPollOption(text = option1)),
                                type = 'quiz',
                                explanation = d['third']['explanation'], 
                                explanation_entities = [MessageEntity(type = 'text_mention', offset = 0, length = len(d['third']['explanation']), user = User(id = poll.explanation_entities[0].user.id, is_bot = False, first_name = 'vad'))]                        
                                )
            d['third'] = 0
            await storage.redis.set(name = str(poll.explanation_entities[0].user.id)+ '_quiz', value = json.dumps(d), ex = 60)
        else:
            await bot.send_message(chat_id = poll.explanation_entities[0].user.id, text =f"правильно ответил: {d['ans']}")
    except:
        pass

            # обнуление counter
    #poll.explanation = 'затерли но передали'


    #await bot.send_message(chat_id = poll_answer.user.id, text = f'poll id{poll_answer.poll_id}, option_ids: {poll_answer.option_ids} user {poll_answer.user.id}')
    #await bot.send_poll(chat_id = 155269575, question= f'poll id {poll.id} {poll.question}', options= [input_poll_option.InputPollOption(text= 'impossible', voter_count = 10), input_poll_option.InputPollOption(text= 'inappropriate', voter_count= 10), input_poll_option.InputPollOption(text= 'inevitable', voter_count= 10)], correct_option_id= 0, type = 'quiz')
    #await bot.forward_message(chat_id= '@eng_poll', from_chat_id = poll_answer.user.id, message_id = 4007)

@router.message(Command('regular'))
async def cmd_regular(message: Message):
    await rq.retrieve_three_regulars(Regular , 1, message.from_user.id, storage = storage, bot = bot)
    

@router.poll_answer()
async def poll_answer_handler(poll_answer: PollAnswer):
    message_id = await storage.redis.get(name = str(poll_answer.user.id) + '_regular_id')
    await bot.stop_poll(chat_id = poll_answer.user.id, message_id = message_id, reply_markup= kb.choice)
    print(type(poll_answer.option_ids))
    d = await storage.redis.get(name = str(poll_answer.user.id) + '_regular')
    d = json.loads(d.decode())
    if d['firstans']:
        print(type(poll_answer.option_ids))
        print(type(d['firstans']))
        if poll_answer.option_ids == json.loads(d['firstans']):
            d['ans'] += 1
        d['firstans'] = 0  
    
    elif d['secondans']:
        if poll_answer.option_ids == json.loads(d['secondans']):
            d['ans'] += 1
        d['secondans'] = 0  
    else:
        if poll_answer.option_ids == json.loads(d['thirdans']):
            d['ans'] += 1
        d['thirdans'] = 0 

    
    if d['second']:
        options = []
        for x, y in d['second'].items():
            if x.startswith('option') and y:
                options.append(input_poll_option.InputPollOption(text= d['second'][x]))
        object_poll = await bot.send_poll(  chat_id= poll_answer.user.id,
                                            question= d['second']['question'], 
                                            open_period = d['second']['open_period'], 
                                            options= options, 
                                            type = 'regular',
                                            is_anonymous= False,
                                            allows_multiple_answers = True                       
                                            )
        d['second'] = 0
        await storage.redis.set(name = str(poll_answer.user.id)+ '_regular_id', value = object_poll.message_id , ex = 60)
    elif d['third']:
        options = []
        for x, y in d['third'].items():
            if x.startswith('option') and y:
                options.append(input_poll_option.InputPollOption(text= d['third'][x]))
        object_poll = await bot.send_poll(  chat_id= poll_answer.user.id,
                                            question= d['third']['question'], 
                                            open_period = d['third']['open_period'], 
                                            options= options, 
                                            type = 'regular',
                                            is_anonymous= False,
                                            allows_multiple_answers = True                       
                                            )
        d['third'] = 0
        await storage.redis.set(name = str(poll_answer.user.id)+ '_regular_id', value = object_poll.message_id , ex = 60)
    else:
        await bot.send_message(chat_id = poll_answer.user.id, text =f"правильно ответил: {d['ans']}")

    await storage.redis.set(name = str(poll_answer.user.id)+ '_regular', value = json.dumps(d), ex = 60)
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


@router.callback_query(Control.filter(F.mark == 'pr'))
async def my_callback(query: CallbackQuery, callback_data: Control):
    if callback_data.ans == '0': # нулевой индекс всегда правильный ответ(лист перемешан)
        callback_data.rightans += 1
        await query.answer("✅✅✅")
    else:
        await query.answer("❌❌❌")

    if callback_data.id%10 == 0:
        await rq.db_helper(query.from_user.id, task_param = 'present_level_time', stars = int(callback_data.rightans), level = round(callback_data.rightans/100, 2), task_level = str(callback_data.id) + ' 0')
        await query.message.edit_text(text=f'Тест пройден. Здесь анализ ответов исходя из  {callback_data.rightans}') # написать функцию
    else:    
        await query.message.edit_text(text= await rq.three_options_sentence(callback_data.id + 1, Present_Past), reply_markup= await rq.three_options_keyboard('pr', callback_data.id + 1, Present_Past, callback_data.rightans))

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

   
@router.callback_query(Conditionals.filter(F.mark == 'pr' or F.mark == 't'))
async def my_callback(query: CallbackQuery, callback_data: Conditionals):
    if callback_data.mark == 'pr':
        table = Present_Past_Compile
    listt = callback_data.keyboard.split(',')
    if  not callback_data.firstans or not callback_data.secondans:
        await query.message.edit_text('Выбери пары из левой и правой колонки по смыслу', reply_markup= await rq.test(table, callback_data.id, listt, callback_data.firstans, callback_data.secondans, callback_data.rightans, callback_data.falseans))
        await query.answer("...")
    elif int(callback_data.firstans[-1]) == int(callback_data.secondans[-1]) - 4:
        listt.remove(callback_data.firstans)
        listt.remove(callback_data.secondans)
        if len(listt) > 2:
            await query.message.edit_text('Выбери пары из левой и правой колонки по смыслу', reply_markup= await rq.test(table, callback_data.id, listt, '', '', callback_data.rightans + 1, callback_data.falseans))
            await query.answer("✅✅✅")
        else:
            if callback_data.id % 3 == 0: # если номер теста заканчивается на 0 или 5 question_level_time
                #callback_data.rightans += 1 добавить балл аза последнюю пару
                rightans = callback_data.rightans - callback_data.falseans
                await rq.db_helper(query.from_user.id, task_param = 'words_level_time', command= 'query')
                if str(int(callback_data.id) - 3) > await rq.db_helper(query.from_user.id, task_param = 'words_level_time', command= 'query'):
                    await query.message.edit_text('Урок уже был пройден')
                elif rightans > 0:
                    await rq.db_helper(query.from_user.id, task_param = 'words_level_time', stars = rightans, level = rightans/100, task_level = 3)
                    await query.message.edit_text(f'Урок пройден. Плюс {rightans}⭐') # уровень и время тоже надо записать 
                else:
                    await rq.db_helper(query.from_user.id, task_param = 'words_level_time', task_level = 3)
                    await query.message.edit_text(f'Урок пройден. Звезд не начислено') # уровень и время тоже надо записать
            else:
                await query.message.edit_text('Выбери пары из левой и правой колонки по смыслу', reply_markup= await rq.test(table, callback_data.id + 1, None, '', '', callback_data.rightans + 1, callback_data.falseans))
                await query.answer("next...")

    else:
        await query.message.edit_text('Выбери пары из левой и правой колонки по смыслу', reply_markup= await rq.test(table, callback_data.id, listt, '', '', callback_data.rightans, callback_data.falseans + 1))
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
    voice = State()


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






