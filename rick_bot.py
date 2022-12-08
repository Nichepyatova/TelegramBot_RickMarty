from aiogram import Bot, Dispatcher, types, executor
import requests
import logging
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_main = InlineKeyboardButton('Рики Морти ', callback_data="rick")
geek_but = InlineKeyboardMarkup().add(button_main)

API_TOKEN = "5733391290:AAFzEA5uoHcqektP4tVDOb6btth2ybDNfDE"


logging.basicConfig(level=logging.INFO)
#initialiing bot and dispatcher
bot = Bot(token=API_TOKEN)
#изменения бота
dp = Dispatcher(bot)
page = 1

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    url1 = "https://rickandmortyapi.com/api/character"
    global page
    if message.text == 'next':
        page += 1
        url1 += f'?page={page}'
    elif message.text == 'prev':
        page -= 1
        url1 += f'?page={page}'
    data = requests.get(url1).json()
    count_one_page = int(data['info']['pages'])//10
    chararters = data['results'][1:count_one_page]
    greet_kb = InlineKeyboardMarkup()
    for i in chararters:
        button_hi = InlineKeyboardButton(f'{i["name"]}', callback_data=f'{i["url"]}')
        greet_kb.add(button_hi)
    button_next = InlineKeyboardButton(f'Вперед', callback_data='next')
    button_prev = InlineKeyboardButton(f'Назад', callback_data='prev')
    greet_kb.add(button_prev, button_next)
    await message.reply("Привет!\nЯ Рик и Морти Бот.", reply_markup=greet_kb)



#отработка кнопок из callback_data
@dp.callback_query_handler()
async def process_callback(call: types.CallbackQuery):
    episodes = []
    if call.data == 'next':
        call.message.text = 'next'
        await send_welcome(message=call.message)
    elif call.data == 'prev':
        call.message.text = 'prev'
        await send_welcome(message=call.message)
    else:
        user = requests.get(call.data).json()
        episodes.append(user["episode"])
        await bot.send_photo(chat_id=call.from_user.id, photo=user["image"],
                             caption=f'{user["name"]}\n'
                                     f'статус: {user["status"]}\n'
                                     f'Гендер: {user["gender"]}\n'
                                     f'{user["origin"]["name"]}\n'
                                     f'Локация:{user["location"]["name"]}\n'
                                     f'Раса: {user["species"]}')



#input , сообщения, вызванные в старт
@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    print(str(message.from_user))
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



