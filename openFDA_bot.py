#!/usr/bin/env python
"""
Version: 0.0.1
Date: 06/03/2023 12:00
Usage:
    python3 openFDA_bot.py
"""

# pip install pytelegrambotapi
# pip install requests

import telebot
from telebot import types
import requests

bot = telebot.TeleBot('<TOKEN>')
api_key = 'amLEylR42PPdHLntVrfyd6PncxuUTMGWlyQViF5K'
limit = 1


@bot.message_handler(commands=['start'])
def get_start(message):
    bot.send_message(message.chat.id, 'Welcome to OpenFDA_bot💊\nPlease, enter drug name:')
    bot.register_next_step_handler(message, get_choice)
    global drug
    drug = message.text.lower()
    
@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.chat.id, 'I can send you information about drugs from Open FDA API. \
                     \n\n✔️Send /start for start my work.')
    
@bot.message_handler(commands=['stop'])
def get_stop(message):
    bot.send_message(message.chat.id, 'Hope you have got necessary information.\nBye!')

@bot.message_handler(commands=['continue'])
def get_continue(message):
    global drug
    bot.send_message(message.chat.id, f"🔺REMINDER:\nContinue get information about {drug.lower()}")
    keyboard = types.InlineKeyboardMarkup()
    key_description = types.InlineKeyboardButton(text='ℹ Description', callback_data='description')
    keyboard.add(key_description)
    key_indication = types.InlineKeyboardButton(text='🔎 Drug indication', callback_data='indication')
    keyboard.add(key_indication)
    key_warning = types.InlineKeyboardButton(text='⚠ Boxed warning', callback_data='warning')
    keyboard.add(key_warning)
    key_contrindications = types.InlineKeyboardButton(text='⛔ Contrindications', callback_data='contrindications')
    keyboard.add(key_contrindications)
    key_info = types.InlineKeyboardButton(text='⚡ Information for patients', callback_data='info')
    keyboard.add(key_info)
    key_pediatric = types.InlineKeyboardButton(text='👶 Pediatric use', callback_data='pediatric')
    keyboard.add(key_pediatric)
    key_geriatric = types.InlineKeyboardButton(text='👵 Geriatric use', callback_data='pediatric')
    keyboard.add(key_geriatric)
    question = f'Pick what you want to know about:'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)  

@bot.message_handler(commands=['new_drug'])
def get_new_drug(message):
    bot.send_message(message.chat.id, f"Please, enter drug name:")
    bot.register_next_step_handler(message, get_choice)
    global drug
    drug = message.text.lower()
    
def get_choice(message):
    global drug
    drug = message.text.lower()
    global api_key, limit, url
    url = f'https://api.fda.gov/drug/label.json?api_key={api_key}&search=drug_interactions:{drug}&limit={limit}'
    global continue_message
    continue_message = '🔁 Send /continue for get else information about this drug. \
                        \n\n▶ Send /new_drug for get information about other drug. \
                         \n\n⏏ Send /start for enter to the main menu. \
                         \n\n⏹ Send /stop for finish work.'
    if requests.get(url).status_code != 200:
        bot.send_message(message.chat.id, "Unfortunately, I can't find about this drug.\nPlease check name and try again!")
        bot.send_message(message.chat.id, continue_message)
    else:
        keyboard = types.InlineKeyboardMarkup()
        key_description = types.InlineKeyboardButton(text='ℹ Description', callback_data='description')
        keyboard.add(key_description)
        key_indication = types.InlineKeyboardButton(text='🔎 Drug indication', callback_data='indication')
        keyboard.add(key_indication)
        key_warning = types.InlineKeyboardButton(text='⚠ Boxed warning', callback_data='warning')
        keyboard.add(key_warning)
        key_contrindications = types.InlineKeyboardButton(text='⛔ Contrindications', callback_data='contrindications')
        keyboard.add(key_contrindications)
        key_info = types.InlineKeyboardButton(text='⚡ Information for patients', callback_data='info')
        keyboard.add(key_info)
        key_pediatric = types.InlineKeyboardButton(text='👶 Pediatric use', callback_data='pediatric')
        keyboard.add(key_pediatric)
        key_geriatric = types.InlineKeyboardButton(text='👵 Geriatric use', callback_data='geriatric')
        keyboard.add(key_geriatric)
        question = f'Pick what you want to know about:'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global continue_message
    if call.data == 'description':
        bot.send_message(call.message.chat.id, get_description())
        bot.send_message(call.message.chat.id, continue_message)
    elif call.data == 'indication':
        bot.send_message(call.message.chat.id, get_indication())
        bot.send_message(call.message.chat.id, continue_message)
    elif call.data == 'warning':
        bot.send_message(call.message.chat.id, get_warning())
        bot.send_message(call.message.chat.id, continue_message)
    elif call.data == 'contrindications':
        bot.send_message(call.message.chat.id, get_contrindications())
        bot.send_message(call.message.chat.id, continue_message)
    elif call.data == 'info':
        bot.send_message(call.message.chat.id, get_information())
        bot.send_message(call.message.chat.id, continue_message)
    elif call.data =='pediatric':
        bot.send_message(call.message.chat.id, get_pediatric_use())
        bot.send_message(call.message.chat.id, continue_message)
    else:
        bot.send_message(call.message.chat.id, get_geriatric_use())
        bot.send_message(call.message.chat.id, continue_message)
    

def get_description():
    global drug, api_key, limit, url
    response = requests.request('GET', url)
    if 'description' not in response.json()['results'][0].keys():
        return "Unfortunately, I don't have information about this section."
    else:
        return response.json()['results'][0]['description']

def get_indication():
    global drug, api_key, limit, url
    response = requests.request('GET', url)
    if 'indications_and_usage' not in response.json()['results'][0].keys():
        return "Unfortunately, I don't have information about this section."
    else:
        return response.json()['results'][0]['indications_and_usage']

def get_warning():
    global drug, api_key, limit, url
    response = requests.request('GET', url)
    if 'boxed_warning' not in response.json()['results'][0].keys():
        return "Unfortunately, I don't have information about this section."
    else:   
        return response.json()['results'][0]['boxed_warning']

def get_contrindications():
    global drug, api_key, limit, url
    response = requests.request('GET', url)
    if 'contraindications' not in response.json()['results'][0].keys():
        return "Unfortunately, I don't have information about this section."
    else:      
        return response.json()['results'][0]['contraindications'] 

def get_information():
    global drug, api_key, limit, url
    response = requests.request('GET', url)
    if 'information_for_patients' not in response.json()['results'][0].keys():
        return "Unfortunately, I don't have information about this section."
    else:   
        return response.json()['results'][0]['information_for_patients'] 

def get_pediatric_use():
    global drug, api_key, limit, url
    response = requests.request('GET', url)
    if 'pediatric_use' not in response.json()['results'][0].keys():
        return "Unfortunately, I don't have information about this section."
    else: 
        return response.json()['results'][0]['pediatric_use'] 

def get_geriatric_use():
    global drug, api_key, limit, url
    response = requests.request('GET', url)
    if 'geriatric_use' not in response.json()['results'][0].keys():
        return "Unfortunately, I don't have information about this section."
    else: 
        return response.json()['results'][0]['geriatric_use'] 

   
    
if __name__ == "__main__":

    try:
        bot.polling(none_stop=True, interval=0)

    except Exception as e:
        print(str(e))
