from dotenv import load_dotenv
load_dotenv()

import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

import sqlite3


BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# creating class for work with DateBase

class DateBase:
    def __init__(self):
        self.conn = sqlite3.connect("tasks.db")
        self.create_table()

    # creating a db table for saving datas
    def create_table(self):
        item = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL
            );
        """
        self.conn.execute(item)
        self.conn.commit()

    # adding tasks
    def add_task(self, title, description):
        item = "INSERT INTO tasks (title, description) VALUES (?, ?)"
        self.conn.execute(item, (title, description))
        self.conn.commit()

     # list of all taks
    def get_all_tasks(self):
        query = "SELECT * FROM tasks"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    # close db
    def close(self):
        self.conn.close()

db = DateBase()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello, i am bot to make your life better. My name is To Do list! \n"
                        "There are several commands: \n"
                        "/add <task> - adding task into list \n"
                        "/list - list of tasks \n")

# Команда /add
@dp.message_handler(commands=['add'])
async def add_task(message: types.Message):
    task = message.text.replace('/add', '').strip()
    if task:
        db.add_task(task, "")
        await message.reply(f"Task '{task}' has been added successfully")
    else:
        await message.reply("You need to write text of tasks")



# Команда /list
@dp.message_handler(commands=['list'])
async def show_list(message: types.Message):
    tasks = db.get_all_tasks()
    if tasks:
        list_text = "List of tasks:\n"
        for idx, task in enumerate(tasks, start=1):
            list_text += f"{idx}.{task[1]}\n"
        await message.reply(list_text)
    else:
        await message.reply("Oops, list of tasks is empty")




@dp.message_handler()
async def echo(message: types.Message):
    await message.reply("Unknown command. Type /start to see the Hello message ")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
