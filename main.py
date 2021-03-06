import asyncio
from pyrogram import Client
from aiogram import Bot, Dispatcher, executor, types
from random import randint
from config import api_id, api_hash, api_token, buffer_chat_id, stock_chat_id, update_time
from time import time

stock = []
last_update = int(time())
bot = Bot(token=api_token)
dp = Dispatcher(bot)
app = Client("my_account", no_updates=True)


async def get_random_photo_from_stock(chat_id):
    global stock, last_update
    if(int(time()) - last_update > update_time or stock == []):
        async with app:
            last_update = time()
            stock = []
            async for message in app.get_chat_history(stock_chat_id):
                if message.photo != None:
                    stock.append(message)
    async with app:
        rand = randint(0, len(stock) - 1)
        await app.send_photo(buffer_chat_id, stock[rand].photo.file_id, str(chat_id))


@dp.message_handler(commands=["mem"])
async def command_handler(message: types.Message):
    await get_random_photo_from_stock(message.chat.id)


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def buffer_handler(message: types.Message):
    if message.chat.id == buffer_chat_id:
        send_to = int(message.caption)
        await bot.send_photo(send_to, message.photo[len(message.photo) - 1].file_id)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
