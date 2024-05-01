import telebot 
from genta import GentaAPI
import os
from dotenv import load_dotenv
import json
# loading variables from .env file
load_dotenv() 
import requests
import json
from openai import OpenAI

# this part is for RAG
url = 'https://4dh8jbxq2gbxjs-8000.proxy.runpod.net/complete'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
    "model_id": "72c7e262083b192e47449eb203dbe5aa5e6e3b7e4b492a0b8f81f761269d3332",
    "completion_parameters": {
        "prompt": [
            {
                "role": "user",
                "content": "Anda adalah asisten AI customer service berbahasa Indonesia yang membantu menjawab pertanyaan serta menyelesaikan permasalahan yang dialami oleh user menggunakan referensi yang tersedia sebagai acuan.\n\n## CONTEXT\nTutorial Integrasi Google Form dengan Woowa Eco\n\nmasuk ke Google Formulir Anda 2. buat formulir baru\n\nbuat spreadsheet dengan memilih tab responses dan kemudian mengklik icon spreadsheet\n\nubah scriptnya, dengan cara klik menu tools >> script editor\n\nsilahkan buka api.woowa.com untuk mendapatkan scriptnya atau bisa melalui link ini\n\nedit apa yang , dan jangan edit apa yang\n\nTutorial Integrasi Woowa Eco X Zapier Dengan Google Form\n\nSilahkan buat google form anda sendiri, pastikan ada kolom untuk mengisi nomor whatsapp\n\nKlik tab '\''Responses'\'' pada google form anda, kemudian klik icon spreadsheet lalu klik '\''Create'\'' untuk membuat spreadsheet responses dari google form yang anda buat\n\nTutorial Integrasi Woowandroid X Google Form\n\nMasuk ke Google Form anda, lalu buatlah form baru\n\nKlik tab reponses lalu buat spreadsheet baru dengan cara: kemudian akan terbuka tab google spreadsheet baru di browser anda\n\n## QUESTION\nBagaimana saya dapat membuat google form di woowa?"
            }
        ],
        "max_new_tokens": 2048,
        "min_length": 8,
        "temperature": 0.7,
        "top_p": 0,
        "random_seed": 0,
        "streaming": False
    }
}


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
            chats.append({"role": "assistant", "content": "Hi there, I am a simple Telegram bot. How can I help you?"})
        
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
        client = OpenAI(
            base_url="https://api.genta.tech",
            api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJDWVlEb2dvaWJyVFRBUnpHWmo3N25qdzJ3MnpwUmhJMSIsImVtYWlsIjoicmVzZWFyY2hzb2NhQGdtYWlsLmNvbSJ9.g9lSqvYx58fZsf9q36_LWC47vd1KoI6QmzQKJ9MPwqw",
        )
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
                    completion = client.chat.completions.create(
                        model="Meta-Llama-3-8B-Instruct",
                        messages=chats,
                        max_tokens=2048
                    )
                    response = completion.choices[0]
                    #print(response)
                    #response_txt = response.json()['text']
                    response_txt = response.message.content
                    print(response_txt)
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