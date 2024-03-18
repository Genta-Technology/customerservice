import telebot 
from genta import GentaAPI
import os
from dotenv import load_dotenv
import json
# loading variables from .env file
load_dotenv() 


def run_telegram_bot(telegram_token:str, prompt:str, genta_token:str, model_name:str):
    """_summary_

    Args:
        telegram_token (str): token from telegram, got from https://t.me/BotFather 
        prompt (str): prompt engineering to user
        genta_token (str): token from genta API
        model_name (str): name of model
    """
    user_data = json.load(open("chat_history.json", "r"))
    
    GENTA_API = GentaAPI(token=genta_token)
    bot = telebot.TeleBot(telegram_token)
    chats = [{"role": "system", "content":prompt}]
    @bot.message_handler(commands=['start']) # Start the message
    
    
    def send_welcome(message):
        bot.reply_to(message, "Hi there, I am a simple Telegram bot. How can I help you?")
        chat_ids = [data["chat_id"] for data in user_data["data"]]
        if message.chat.id in chat_ids:
            index_chat_id = chat_ids.index(message.chat.id)
            chats = user_data["data"][index_chat_id]["chat_history"]
        else: 
            chats = [{"role": "system", "content":prompt}]
        if len(chats) == 1:
            chats.append({"role": "user", "content": "Hi there, I am a simple Telegram bot. How can I help you?"})
            user_data["data"].append({
                "chat_id": message.chat.id,
                "time_last_conversation": message.date,
                "chat_history": chats
            })
        json.dump(user_data, open("chat_history.json", "w"))

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

    @bot.message_handler(commands=["checkstatus"])
    def send_status(message):
        bot.reply_to(message, str(user_data))
    
    
    @bot.message_handler(func=lambda message: True)  # Respond to all other messages
    def echo_all(message):
        user_data = json.load(open("chat_history.json", "r"))
        #print(message.chat.id)
        chat_ids = [data["chat_id"] for data in user_data["data"]]
        if message.chat.id in chat_ids:
            index_chat_id = chat_ids.index(message.chat.id)
            chats = user_data["data"][index_chat_id]["chat_history"]
        else: 
            chats = [{"role": "system", "content":prompt}]
        if len(chats)/2 <= user_data["max_chat_size"] and user_data["bot_status"]:
            user_response = {"role": "user", "content": message.text}
            chats.append(user_response)
            while (True):
                try:
                        
                    response = GENTA_API.ChatCompletion(chat_history=chats,
                                                        model_name=model_name,
                                                        temperature=user_data["temperature"],
                                                        max_new_tokens=user_data["max_token"])
                    response_txt = response[0][0][0]['generated_text']
                    chat = {"role": "assistant", "content": response_txt}
                    chats.append(chat)
                    bot.reply_to(message, response_txt)
                    
                    
                    if message.chat.id in chat_ids:
                        index_chat_id = chat_ids.index(message.chat.id)
                        user_data["data"][index_chat_id]["time_last_conversation"] = message.date
                        user_data["data"][index_chat_id]["chat_history"] = chats
                    else:
                        user_data["data"].append({
                            "chat_id": message.chat.id,
                            "time_last_conversation": message.date,
                            "chat_history": chats
                        })
                    json.dump(user_data, open("chat_history.json", "w"))
                    break
                except Exception as e:
                    print(e)
                    bot.reply_to(message, "waiting for Model to scale up")
                    continue
        elif not user_data["bot_status"]:
            bot.reply_to(message, "sorry currently this bot is not available")
        elif len(chats)/2 > user_data["max_chat_size"]:
            bot.reply_to(message, "sorry you have reached the maximum chat ammount")
            
        
    bot.infinity_polling()
    
if __name__ == "__main__":
    user_data = json.load(open("chat_history.json", "r"))
    run_telegram_bot(telegram_token= user_data["telegram_bot_token"],
                 model_name='OpenChat-7B',
                 prompt="You are a friendly and helpful assistant",
                 genta_token= user_data["genta_token"])