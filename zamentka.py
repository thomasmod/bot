from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

TOKEN = '6567194474:AAGKjA_a9clchbPjs1TrfuCSN57HBmGcg5I'
NOTES_DIRECTORY = 'notes'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот "Заметка". Используй команды /save, /get и /all для работы с заметками.')

def save_note(update: Update, context: CallbackContext) -> None:
    try:
        _, filename, *text = context.args
        note_text = ' '.join(text)
        os.makedirs(NOTES_DIRECTORY, exist_ok=True)
        with open(os.path.join(NOTES_DIRECTORY, filename), 'w') as note_file:
            note_file.write(note_text)
        update.message.reply_text(f'Заметка "{filename}" успешно сохранена.')
    except ValueError:
        update.message.reply_text('Используйте команду /save <filename> <текст> для сохранения заметки.')

def get_note(update: Update, context: CallbackContext) -> None:
    try:
        _, filename = context.args
        with open(os.path.join(NOTES_DIRECTORY, filename), 'r') as note_file:
            note_text = note_file.read()
        update.message.reply_text(f'Заметка "{filename}":\n{note_text}')
    except FileNotFoundError:
        update.message.reply_text(f'Заметка "{filename}" не найдена.')
    except ValueError:
        update.message.reply_text('Используйте команду /get <filename> для получения заметки.')

def list_notes(update: Update, context: CallbackContext) -> None:
    notes_list = os.listdir(NOTES_DIRECTORY)
    if notes_list:
        notes_text = "\n".join(notes_list)
        update.message.reply_text(f'Список сохраненных заметок:\n{notes_text}')
    else:
        update.message.reply_text('Нет сохраненных заметок.')

def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("save", save_note))
    dp.add_handler(CommandHandler("get", get_note))
    dp.add_handler(CommandHandler("all", list_notes))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
