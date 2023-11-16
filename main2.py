import telebot
from datetime import datetime, timedelta
from pytz import timezone  # pytz kutubxonasini qo'shing
import time

# Botni tokenini quyidagi o'rniga joylashtiring
TOKEN = "6751568339:AAFBsO1Jex2szUO7uQ9eGRaagj7y0r5KZT8"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Assalomu alaykum! Yangi yilga qolgan vaqt hisoblovchi botga xush kelibsiz!')

@bot.message_handler(commands=['time_left'])
def handle_time_left(message):
    # O'zbekiston vaqti (Qarshi)
    qarshi_tz = timezone('Asia/Qarshi')
    current_time = datetime.now(qarshi_tz)
    
    # Yangi yil vaqti
    new_year = datetime(current_time.year + 1, 1, 1, 0, 0, 0, tzinfo=qarshi_tz)
    
    # Vaqt farqi
    time_left = new_year - current_time

    days_left = time_left.days
    hours_left, remainder = divmod(time_left.seconds, 3600)
    minutes_left, seconds_left = divmod(remainder, 60)

    time_left_str = f"Yangi yilga {days_left} kun, {hours_left} soat, {minutes_left} daqiqa va {seconds_left} soniya qoldi!"
    bot.send_message(message.chat.id, time_left_str)

# Обработчик команды /ping
@bot.message_handler(commands=['ping'])
def ping(message):
    start_time = time.time()
    bot.send_message(message.chat.id, "Pong!")
    end_time = time.time()
    ping_time = end_time - start_time
    bot.send_message(message.chat.id, f"Ping time: {ping_time} seconds")

if __name__ == "__main__":
    bot.polling(none_stop=True)
