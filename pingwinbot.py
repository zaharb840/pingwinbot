import telebot
from telebot import types
import time
import threading
from threading import Timer
from telebot.types import ChatPermissions

TOKEN = '7158222093:AAEABzINhhlYiBdltEVOLqKe7Kkg-jTs-qs'
bot = telebot.TeleBot(TOKEN)

welcomemessage = "Добро пожаловать в нашу уютную Партию Линуксоидов и Юниксоидов СНГ!. Здесь мы обсуждаем различные вещи связанные с Linux."

@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def welcome_new_member(message):
    bot.reply_to(message, welcomemessage)

def is_user_admin(chat_id, user_id):
    """Проверка, является ли пользователь администратором в чате."""
    admin_list = bot.get_chat_administrators(chat_id)
    return any(admin.user.id == user_id for admin in admin_list)

@bot.message_handler(commands=['ban'])
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


@bot.message_handler(commands=['report'])
def handle_report(message):
    bot.reply_to(message, '@mustdieie150, братан, тебе тут выписали вызов!')

bot.polling(none_stop=True)
