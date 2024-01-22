import os
import logging
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.environ.get('BOT_KEY')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

room_capacity = 5
queue = []


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in queue:
        queue.append(user_id)
        await message.reply(f'Вы добавлены в очередь. Ваш номер: {len(queue)}')
        if len(queue) == 1:
            await notify_next_user()


@dp.message_handler(commands=['take_customer'])
async def take_customer(message: types.Message):
    user_id = message.from_user.id
    if user_id == queue[0]:
        queue.pop(0)
        await message.reply('Вы взяли клиента. Ждите следующего уведомления.')
        await notify_next_user()
    else:
        await message.reply('Не ваша очередь взять клиента.')


async def notify_next_user():
    if queue:
        next_user_id = queue[0]
        await bot.send_message(next_user_id, 'Ваша очередь взять клиента.')

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
