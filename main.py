import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.utils import executor
from parse import get_pharmacies

# Инициализация бота и диспетчера
TOKEN = '6029249401:AAGFsrmGk_sdmuiT6bW6MPdAQzBdu6gJpeA'
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот поиска лекарств в аптеках. Введите название лекарства.")


# Обработчик сообщений
@dp.message_handler()
async def search_drug(message: types.Message):
    drug_name = message.text
    pharmacies = get_pharmacies(drug_name)
    with open("drugs_dict.json", 'r', encoding='UTF-8') as file:
        drugs_dict = json.load(file)
    if len(drugs_dict) == 0:
        await message.reply("Ничего не найдено! Попробуйте снова")
    for k, v in (drugs_dict.items()):
        drugs = f"{hlink(v['drugs_title'], v['drugs_url'])}\n" \
                f"Цена: {hbold(v['drugs_price'])} RUB\n" \
                f"Наличие на складе: {hbold(v['drugs_available'])}"
        await message.reply(drugs)


if __name__ == '__main__':
    executor.start_polling(dp)
