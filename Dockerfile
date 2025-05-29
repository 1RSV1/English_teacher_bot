FROM python:3.10.17-bookworm

WORKDIR /app
COPY . . 
RUN pip install asyncpg SQLAlchemy aiogram python-dotenv requests openai pydub gtts aiosqlite
RUN python bot.py
