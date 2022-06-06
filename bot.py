import telebot
import requests
from telebot import custom_filters
import telebot
from telebot.types import InlineKeyboardButton, CallbackQuery,InlineKeyboardMarkup,BotCommand
from telebot.handler_backends import State, StatesGroup

from telebot.storage import StateMemoryStorage

URL_REGISTRASI = "https://simpeg.tegalkota.go.id/simpegonline_bot/ajax_registrasi_sinokbot/{nip}/{password}/{id}/{name}"
URL_HAPUS = "https://simpeg.tegalkota.go.id/simpegonline_bot/ajax_del_IDsinokbot/{nip}/{password}/{id}"

state_storage = StateMemoryStorage()

bot = telebot.TeleBot("5372477509:AAGoMYmPk-258WFot4uiZfpXofvLGdKb2y4", 
                      parse_mode=None,state_storage=state_storage)

bot.set_my_commands([
    BotCommand("/start", "Menu utama")
])

class State(StatesGroup):
    isAuth = State()

user_dict = {}

class User:
    nip = ""
    password = ""

def main_menu():
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text='🏢 Registrasi dulu kuy!',
                    callback_data='registrasi'
                ),
                 InlineKeyboardButton(
                    text='🛢 Hapus akun',
                    callback_data='hapus'
                )
            ]
        ]
    )
    
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Selamat datang !",reply_markup=main_menu())    

@bot.callback_query_handler(func=lambda c: c.data == "registrasi")
def registrasi_callback(call: CallbackQuery):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='🙂 Silahkan Masukkan NIP')
    bot.register_next_step_handler_by_chat_id(call.message.chat.id,regist_nip)

def regist_nip(message):
    user = User()
    user.nip = message.text
    user_dict[message.chat.id] = user
    
    bot.send_message(message.chat.id,"🔑 Silahkan Masukkan Password")
    bot.register_next_step_handler_by_chat_id(message.chat.id,regist_password)

def regist_password(message):
    user = user_dict[message.chat.id]
    user.password = message.text
    try:
        request_url = URL_REGISTRASI.format(nip=user.nip,password=user.password,id=message.chat.id,name=message.from_user.full_name)
        call = requests.get(request_url)
        result = call.json()
        if(result['status'] == 1 or result['status'] == 4):
            bot.send_message(message.chat.id, result['pesan'])
            bot.set_state(message.from_user.id, State.isAuth, message.chat.id)
        else:
            bot.send_message(message.chat.id, result['pesan'])
            bot.send_message(message.chat.id, "🔄 Silahkan mengulangi kembali.",reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, "‼️🛑 Server Error")
        bot.send_message(message.chat.id, "🔄 Silahkan mengulangi kembali.",reply_markup=main_menu())

@bot.callback_query_handler(func=lambda c: c.data == "hapus")
def hapus_callback(call: CallbackQuery):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='🙂 Silahkan Masukkan NIP')
    bot.register_next_step_handler_by_chat_id(call.message.chat.id,hapus_nip)

def hapus_nip(message):
    user = User()
    user.nip = message.text
    user_dict[message.chat.id] = user
    
    bot.send_message(message.chat.id,"🔑 Silahkan Masukkan Password")
    bot.register_next_step_handler_by_chat_id(message.chat.id,hapus_password)

def hapus_password(message):
    user = user_dict[message.chat.id]
    user.password = message.text
    try:
        request_url = URL_HAPUS.format(nip=user.nip,password=user.password,id=message.chat.id)
        call = requests.get(request_url)
        result = call.json()
        if(result['status'] == 1):
            bot.send_message(message.chat.id, result['pesan'])
            bot.delete_state(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.chat.id, result['pesan'])
            bot.send_message(message.chat.id, "🔄 Silahkan mengulangi kembali.",reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, "‼️🛑 Server Error")
        bot.send_message(message.chat.id, "🔄 Silahkan mengulangi kembali.",reply_markup=main_menu())
    
@bot.message_handler(state=State.isAuth)
def send_text(message):
    bot.send_message(message.chat.id, "Anda sedanga berkomunikasi dengan bot")

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

bot.infinity_polling()