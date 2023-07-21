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
                description TEXT NOT NULL,
                isdone BOOLEAN NOT NULL
            );
        """
        self.conn.execute(item)
        self.conn.commit()

    # adding tasks
    def add_task(self, title, description):
        item = "INSERT INTO tasks (title, description, isdone) VALUES (?, ?, 0)"
        self.conn.execute(item, (title, description))
        self.conn.commit()

     # list of all taks
    def get_alltasks(self):
        item = "SELECT * FROM tasks"
        cursor = self.conn.execute(item)
        return cursor.fetchall()

    # deleting tasks
    def delete_task(self, task_id):
        item = "DELETE FROM tasks WHERE id = ?"
        self.conn.execute(item, (task_id,))
        self.conn.commit()

    # isdone
    def mark_done(self, task_id):
        item = "UPDATE tasks SET isdone = 1 WHERE id = ?"
        self.conn.execute(item, (task_id,))
        self.conn.commit()

    # close db
    def close(self):
        self.conn.close()

db = DateBase()


@dp.message_handler(commands=['start'])
async def send_hello(message: types.Message):
    await message.reply(""" Hello, i am bot to make your life better. \nMy name is To Do list! \n
                        There are several commands: \n
                        /start - welcome message \n
                        /add <task> - adding task into list \n
                        /done <task> - mark task as done \n
                        /list - list of tasks \n
                        /delete <task> - delete the task by id \n
                        """)

# /add command
@dp.message_handler(commands=['add'])
async def add_task(message: types.Message):
    task = message.text.replace('/add', '').strip()
    if task:
        db.add_task(task, "")
        await message.reply(f"Task '{task}' has been added successfully")
    else:
        await message.reply("You need to write text of tasks")



# /list command
@dp.message_handler(commands=['list'])
async def show_list(message: types.Message):
    tasks = db.get_alltasks()
    if tasks:
        task_list = "List of tasks:\n"
        for idx, task in enumerate(tasks, start=1):
            istaskdone = "✅" if task[3] else "❌"
            mark = "🔖"
            task_list += f"{mark} {idx}. {task[1]} {istaskdone}\n"
        await message.reply(task_list)
    else:
        await message.reply("Oops, list of tasks is empty")

# /delete commad
@dp.message_handler(commands=['delete'])
async def delete_task(message: types.Message):
    try:
        task_id = int(message.text.replace('/delete', '').strip())
        tasks = db.get_alltasks()
        if 1 <= task_id <= len(tasks):
            db.delete_task(task_id)
            await message.reply(f"Task '{tasks[task_id - 1][1]}' has been deleted")
        else:
            await message.reply("Incorrect id")
    except ValueError:
        await message.reply("You need to write id")

@dp.message_handler(commands=['done'])
async def mark_done(message: types.Message):
    try:
        task_id = int(message.text.replace('/done', '').strip())
        tasks = db.get_alltasks()
        if 1 <= task_id <= len(tasks):
            db.mark_done(task_id)
            await message.reply(f"Task '{tasks[task_id - 1][1]}' has been marked successfully")
        else:
            await message.reply("Incorrect id")
    except ValueError:
        await message.reply("You need to write id")




@dp.message_handler()
async def echo(message: types.Message):
    await message.reply("Unknown command. Type /start to see the Hello message ")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
