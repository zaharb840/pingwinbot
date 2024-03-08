import telebot
from telebot import types
import time
import threading
from threading import Timer
from telebot.types import ChatPermissions

TOKEN = 'YOUR_TOKEN_HERE'
bot = telebot.TeleBot(TOKEN)

welcomemessage = "Добро пожаловать в наш уютный Linux Чат🐧. Здесь мы обсуждаем различные вещи связанные с Linux. Прочитайте правила чата в закрепе. Незнание их не освобождает от ответственности!"

@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def welcome_new_member(message):
    bot.reply_to(message, welcomemessage)

def is_user_admin(chat_id, user_id):
    """Проверка, является ли пользователь администратором в чате."""
    admin_list = bot.get_chat_administrators(chat_id)
    return any(admin.user.id == user_id for admin in admin_list)

@bot.message_handler(commands=['ban, kick'])
def handle_ban(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not is_user_admin(chat_id, user_id):
        bot.reply_to(message, "Ты чё, хакер чтоли? Только администраторы могут использовать эту команду.")
        return

    if message.reply_to_message:
        user_to_ban = message.reply_to_message.from_user.id
        try:
            bot.kick_chat_member(chat_id, user_to_ban)
            bot.reply_to(message, "Пользователь забанен/кикнут.")
        except Exception as e:
            bot.reply_to(message, f"Упс... Не могу забанить/кикнуть пользователя: {e}")
    else:
        bot.reply_to(message, "Ответьте на сообщение пользователя, которого хотите забанить/кикнуть.")

@bot.message_handler(commands=['mute'])
def handle_mute(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not is_user_admin(chat_id, user_id):
        bot.reply_to(message, "Ты чё, хакер чтоли? Только администраторы могут использовать эту команду.")
        return

    if message.reply_to_message:
        user_to_mute = message.reply_to_message.from_user.id
        try:
            bot.restrict_chat_member(chat_id, user_to_mute, can_send_messages=False)
            bot.reply_to(message, "Этот пользователь депортирован в сМУТу.")
        except Exception as e:
            bot.reply_to(message, f"Упс... Не могу дать 'мут' пользователю: {e}")
    else:
        bot.reply_to(message, "Ответьте на сообщение пользователя, которому хотите дать 'мут'.")

def unmute_user(chat_id, user_id):
    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True
    )
    bot.restrict_chat_member(chat_id, user_id, permissions=permissions)

def temp_mute_user(chat_id, user_id, mute_duration):
    permissions = ChatPermissions(can_send_messages=False)
    bot.restrict_chat_member(chat_id, user_id, permissions=permissions)
    bot.send_message(chat_id, f"Пользователь замучен на {mute_duration} секунд.")

    Timer(mute_duration, unmute_user, args=(chat_id, user_id)).start()

@bot.message_handler(commands=['tmute'])
def handle_temp_mute(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.from_user.id

        if not is_user_admin(chat_id, user_id):
            bot.reply_to(message, "Только администраторы могут использовать эту команду.")
            return

        command_parts = message.text.split()
        if len(command_parts) == 2 and command_parts[1].isdigit():
            mute_seconds = int(command_parts[1])
            user_to_mute = message.reply_to_message.from_user.id

            permissions = types.ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False
            )
            bot.restrict_chat_member(chat_id, user_to_mute, permissions)
            
            bot.reply_to(message, f"Пользователь был депортирован в сМУТу на {mute_seconds} секунд.")

            threading.Thread(target=unmute_user, args=(chat_id, user_to_mute)).start()
        else:
            bot.reply_to(message, "Ошибка в команде. Используйте /tmute <количество_секунд>.")
    else:
        bot.reply_to(message, "Эту команду нужно отправить ответом на сообщение пользователя.")


@bot.message_handler(commands=['report'])
def handle_report(message):
    bot.reply_to(message, '@mustdieie150, братан, тебе тут выписали вызов!')

bot.polling(none_stop=True)
