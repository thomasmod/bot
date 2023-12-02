import os
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from pyppeteer import launch

API_TOKEN = "6567194474:AAGKjA_a9clchbPjs1TrfuCSN57HBmGcg5I"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def take_screenshot(url, filename):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    await page.screenshot({'path': filename})
    await browser.close()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Этот бот делает скриншоты сайтов. Используйте команду /screenshot <URL> для получения скриншота.")

@dp.message_handler(commands=['screenshot'])
async def make_screenshot(message: types.Message):
    try:
        # Получаем URL из команды
        _, url = message.text.split(' ', 1)
        
        # Генерируем имя файла
        filename = f"{message.from_user.id}_screenshot.png"
        
        # Проверяем, что URL начинается с http:// или https://
        if url.startswith(('http://', 'https://')):
            await take_screenshot(url, filename)
            with open(filename, 'rb') as photo:
                await bot.send_photo(message.chat.id, photo, caption=f"Скриншот сайта: {url}")
            os.remove(filename)  # Удаляем временный файл после отправки
        else:
            await message.reply("Пожалуйста, укажите корректный URL, начиная с http:// или https://.")
    except ValueError:
        await message.reply("Используйте команду /screenshot <URL> для получения скриншота сайта.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
