import os
import subprocess
import telebot
from telebot import types

# Устанавливаем токен нашего бота
bot = telebot.TeleBot('6005545859:AAG40U3OHDzY7EaeW1yPCM6WP9grjPs-uQk')

# Создаем хендлер для команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Привет, отправь мне файл .torrent')

# Создаем хендлер для приема файла .torrent
@bot.message_handler(content_types=['document'])
def handle_torrent(message):
    # Скачиваем файл .torrent
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    # Сохраняем файл на диск
    src = 'downloads/' + message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    # Запускаем процесс загрузки торрента
    subprocess.Popen(['transmission-cli', src, '-w', 'downloads'])
    # Отправляем пользователю сообщение об успешной загрузке
    bot.reply_to(message, 'Файл успешно загружен!')

# Создаем хендлер для команды /files
@bot.message_handler(commands=['files'])
def list_files(message):
    # Получаем список загруженных файлов
    files = os.listdir('downloads')
    if not files:
        bot.reply_to(message, 'Нет загруженных файлов')
        return
    # Создаем клавиатуру для выбора файла
    markup = types.InlineKeyboardMarkup()
    for file_name in files:
        button = types.InlineKeyboardButton(text=file_name, callback_data=file_name)
        markup.add(button)
    bot.send_message(message.chat.id, 'Выберите файл для отправки:', reply_markup=markup)

# Создаем хендлер для обработки выбора файла
@bot.callback_query_handler(func=lambda call: True)
def send_file(call):
    # Отправляем выбранный файл пользователю
    file_path = 'downloads/' + call.data
    with open(file_path, 'rb') as file:
        bot.send_document(call.message.chat.id, file)

# Запускаем бота
bot.polling()