FROM python:3.10.17-bookworm

WORKDIR /app
COPY . . 
RUN python -m venv venv
RUN source venv/bin/activate
RUN pip install asyncpg SQLAlchemy aiogram python-dotenv requests openai
RUN python bot.py
