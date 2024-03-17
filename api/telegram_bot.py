import telebot 
from genta import GentaAPI
import os
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 


def run_telegram_bot(telegram_token:str, prompt:str, genta_token:str, model_name:str):
    # Replace with your actual token 
    GENTA_API = GentaAPI(token=genta_token)
    bot = telebot.TeleBot(telegram_token)
    chats = [{"role": "system", "content":prompt}]
    @bot.message_handler(commands=['start']) # Start the message
    def send_welcome(message):
        bot.reply_to(message, "Hi there, I am a simple Telegram bot. How can I help you?")
        chats.append({"role": "user", "content": "Hi there, I am a simple Telegram bot. How can I help you?"})

    @bot.message_handler(commands=['help']) # give help to the user
    def send_help(message):
        bot.reply_to(message,
    """Hi, this is a telegram bot integrated with Genta API.

    You can control me by sending these commands:

    /start - restart your chats from the beginning
    /clear - clear all chats
    """)
        
    @bot.message_handler(commands=['clear']) # Clear all of chat
    def send_help(message):
        chats = []
        bot.reply_to(message, "chat cleared, you could restart your messages")

    @bot.message_handler(func=lambda message: True)  # Respond to all other messages
    def echo_all(message):
        try:
            user_response = {"role": "user", "content": message.text}
            chats.append(user_response)
            response = GENTA_API.ChatCompletion(chats,model_name=model_name)
            response = GENTA_API.ChatCompletion(chat_history=chats, model_name=model_name)
            response_txt = response[0][0][0]['generated_text']
            chat = {"role": "assistant", "content": response_txt}
            chats.append(chat)
            bot.reply_to(message, response_txt)
        except:
            bot.reply_to(message, "sorry Genta API is not available for now")

    bot.infinity_polling()
    
if __name__ == "__main__":
    run_telegram_bot(telegram_token= os.getenv('CHATBOT_TOKEN'),
                 model_name='OpenChat-7B',
                 prompt="You are a friendly and helpful assistant",
                 genta_token=os.getenv('GENTA_API_KEY'))