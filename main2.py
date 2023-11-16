import datetime
from pytz import timezone
from telegram.ext import Updater, CommandHandler, CallbackContext

# Токен вашего бота
TOKEN = "6751568339:AAFBsO1Jex2szUO7uQ9eGRaagj7y0r5KZT8"

# Временная зона Ташкента
tz_tashkent = timezone('Asia/Tashkent')

def time_until_new_year(update, context):
    now = datetime.datetime.now(tz_tashkent)
    new_year = datetime.datetime(now.year + 1, 1, 1, 0, 0, 0, 0, tz_tashkent)
    time_left = new_year - now

    days, seconds = time_left.days, time_left.seconds
    hours = seconds // 3600

    update.message.reply_text(f"До Нового года в Ташкенте осталось {days} дней и {hours} часов.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Обработчик команды /timeleft
    dp.add_handler(CommandHandler("timeleft", time_until_new_year))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
