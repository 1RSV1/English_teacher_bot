FROM python:3.10.17-bookworm

WORKDIR /app
COPY . . 
RUN pip install asyncpg SQLAlchemy aiogram python-dotenv requests openai pydub gtts aiosqlite redis
RUN python bot.py
