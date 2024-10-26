import os
import telebot
import pyzipper
import random
import string

BOT_TOKEN = '7710953815:AAGOBAwnDHSzDxhj3qjkRnvWZKlje1hBehY'
bot = telebot.TeleBot(BOT_TOKEN)

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    login = message.text
    password = generate_password()
    archive_password = generate_password()

    # Создаем текстовый файл с логином и паролем
    file_content = f"login: {login}\npassword: {password}"
    file_name = f"{login}.txt"
    with open(file_name, 'w') as file:
        file.write(file_content)

    # Создаем архив с паролем
    archive_name = f"{login}.zip"
    with pyzipper.AESZipFile(archive_name, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(archive_password.encode())
        zf.write(file_name)

    # Отправляем архив пользователю
    with open(archive_name, 'rb') as archive:
        bot.send_document(message.chat.id, archive, caption=f"login: `{login}`\npassword: `{password}`\nПароль от архива: `{archive_password}`", parse_mode='Markdown')

    # Удаляем временные файлы
    os.remove(file_name)
    os.remove(archive_name)

if __name__ == '__main__':
    bot.polling(none_stop=True)