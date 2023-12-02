import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram import executor

API_TOKEN = "6567194474:AAGKjA_a9clchbPjs1TrfuCSN57HBmGcg5I"
SAVE_DIRECTORY = "saved_files"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Этот бот сохраняет различные файлы. Используй команду /save <filename> для сохранения и /all для просмотра сохраненных файлов.")

@dp.message_handler(commands=['save'])
async def save_file(message: types.Message):
    try:
        # Получаем параметры из команды
        _, filename = message.text.split(' ', 1)
        
        # Проверяем, есть ли файлы в сообщении
        if message.document:
            file_id = message.document.file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            downloaded_file = await bot.download_file(file_path)
            
            # Создаем директорию, если ее нет
            os.makedirs(os.path.join(SAVE_DIRECTORY, filename), exist_ok=True)
            
            # Сохраняем файл
            file_full_path = os.path.join(SAVE_DIRECTORY, filename, message.document.file_name)
            with open(file_full_path, 'wb') as new_file:
                new_file.write(downloaded_file.read())
                
            await message.reply(f"Файл '{message.document.file_name}' сохранен в каталоге '{filename}'.")
        else:
            await message.reply("Пожалуйста, отправьте файл для сохранения.")
    except ValueError:
        await message.reply("Используйте команду /save <filename> для сохранения файлов.")

@dp.message_handler(commands=['all'])
async def show_all_files(message: types.Message):
    files_list = []
    
    # Получаем список файлов
    for root, dirs, files in os.walk(SAVE_DIRECTORY):
        for file in files:
            files_list.append(os.path.join(root, file))
    
    # Отправляем список файлов
    if files_list:
        files_text = "\n".join(files_list)
        await message.reply(f"Сохраненные файлы:\n{files_text}")
    else:
        await message.reply("Нет сохраненных файлов.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
