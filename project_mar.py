from aiogram import Bot, Dispatcher, executor, types
import subprocess
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



 
API_TOKEN = ''
language = "diffrent"
 
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

button1 = KeyboardButton('mypy')
button2 = KeyboardButton('bandit')

markup3 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button1).add(button2)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply (f"Привет! Я бот для статического анализа кода на языке программирования Python.\nMypy предназначен для проверки правильности использования переменных и функций кода\nBandit предназначен для проверки безопасности выполнения кода",reply_markup=markup3)
    


@dp.message_handler(lambda message: message.text in ["mypy","bandit"])
async def handle_selected_language(message: types.Message):
    global language
    language = message.text
    await message.answer(f"Вы выбрали инструмент {message.text}. Пожалуйста, пришлите файл, написанный на языке программирования Python.")

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_file(message: types.Message):
    response_text = ""
    if message.document:
        file_info = message.document
        file_path = await bot.get_file(file_id=message.document.file_id)
        file_destination = f"{language}/{file_info.file_name}"

        await bot.download_file(file_path=file_path.file_path, destination=file_destination)
        await message.answer(f"Файл {file_info.file_name} получен. Начинается статический анализ кода.\n\
Это может занять несколько минут...")


        command = f"{language} {file_destination}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            response_text = "Статический анализ проведён успешно."
    if stdout:
        response_text += f"\nOutput:\n{stdout.decode()}"
        await message.answer(response_text)
    else:
        response_text = "Во время анализа произошла ошибка :("
        if stderr:
            response_text += f"\nError:\n{stderr.decode()}"
        await message.answer(response_text)


if __name__ == '__main__':
   executor.start_polling(dp)
