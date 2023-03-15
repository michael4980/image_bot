import os
from threading import Thread

import telebot
from telebot.async_telebot import AsyncTeleBot
import cv_filter, client
from database import config


conf = config.load_config(r'database/source.ini')

bot = AsyncTeleBot(token=conf.tg_bot.token)
futures = []

'''User Handlers'''
@bot.message_handler(commands=['start'])
async def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    btn1 = telebot.types.KeyboardButton('Menu')
    markup.add(btn1)
    try:
        client.user_create(message.from_user.id, message.from_user.first_name)
    except Exception as ex:
        text = f"You already registred"
        await bot.send_message(message.chat.id, text, reply_markup=markup)
    text = f'Hi, {message.from_user.full_name}, send image, which u want to edit'
    await bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(regexp='Load Image')
async def loader(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Operations list')
    markup.add(btn1)
    text = f'Waiting for load...'
    await bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(content_types=['photo'])
async def photo_id(message):
    fileID = message.photo[-1].file_id   
    file_info = await bot.get_file(fileID)
    downloaded_file = await bot.download_file(file_info.file_path)
    name = str(message.from_user.id)
    with open(f"images/clear/{name}.png", 'wb') as new_file:
         new_file.write(downloaded_file)
    text = f'Done'
    await bot.send_message(message.chat.id, text)

@bot.message_handler(regexp='Operations list')
async def operation(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Inversion')
    btn2 = telebot.types.KeyboardButton('Sobel_filter')
    btn3 = telebot.types.KeyboardButton('Laplas filter')
    btn4 = telebot.types.KeyboardButton('Blur')
    btn5 = telebot.types.KeyboardButton('Menu')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    text = f'Choose operation'
    await bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(regexp='Menu')
async def menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Load Image')
    btn2 = telebot.types.KeyboardButton('Operations list')
    btn3 = telebot.types.KeyboardButton('My stat')
    markup.add(btn1, btn2, btn3)
    text = f'Main menu'
    await bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(regexp='My stat')
async def menu(message):
    id = message.from_user.id
    try:
        result = client.get_user_by_id(id)
        text = f'Take your info: {result}'
    except Exception as ex:
        text = 'You haven`t opearation yet, choose some from operations'
        print(ex)
    await bot.send_message(message.chat.id, text)

async def filters(func, message):
    markup = telebot.types.ReplyKeyboardMarkup()
    load_photo = os.listdir(r"images/clear")
    name = str(message.from_user.id)
    if f'{name}.png' in load_photo:
        btn1 = telebot.types.KeyboardButton('Menu')
        markup.add(btn1)
        text = f"IN PROGRESS..."
        await bot.send_message(message.chat.id, text, reply_markup= markup)
        path = f"images/clear/{name}.png"
        func(path, name)
        f_name = func.__name__
        stat = os.stat(f"images/result/{name}.png")
        try:
            client.create_operation(f_name, name, stat.st_size, image_name=f'{name}.png')
        except Exception as ex:
            text = f'Something going wrong'
            await bot.send_message(message.chat.id, text)
        text = f'Take your image'
        await bot.send_message(message.chat.id, text)
        await bot.send_photo(message.chat.id, photo= open(f"images/result/{name}.png", 'rb'))
        os.remove(f"images/result/{name}.png")
    else:
        btn1 = telebot.types.KeyboardButton('Load Image')
        btn2 = telebot.types.KeyboardButton('Menu')
        markup.add(btn1, btn2)
        text = f'You need to upload image first'
        await bot.send_message(message.chat.id, text, reply_markup=markup) 


          
@bot.message_handler(regexp='Inversion')
async def invers(message):
    await filters(cv_filter.inversion, message)

@bot.message_handler(regexp='Blur')
async def bluring(message):
    await filters(cv_filter.blur, message)
    
@bot.message_handler(regexp='Laplas filter')
async def laplas(message):
   await filters(cv_filter.laplas_filter, message)
    
@bot.message_handler(regexp='Sobel_filter')
async def sobel(message):
    await filters(cv_filter.sobel_filter, message)

'''Admin handlers'''
@bot.message_handler(func=lambda message: message.from_user.id == int(conf.tg_bot.admin_id) and message.text == "admin")
async def admin_panel(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('User stat')
    btn2 = telebot.types.KeyboardButton('All users')
    btn3 = telebot.types.KeyboardButton('Menu')
    markup.add(btn1, btn2, btn3)
    text = f'Admin bar'
    await bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.from_user.id == int(conf.tg_bot.admin_id) and message.text == 'User stat')
async def user_info(message):
    text = f'Insert telegram id'
    await bot.send_message(message.chat.id, text)
    
@bot.message_handler(func=lambda message: message.from_user.id == int(conf.tg_bot.admin_id), regexp='\d{6,11}')
async def user_result(message):
    try:
        result = client.get_user_by_id(message.text)
        text = f'Take your info: {result}'
    except Exception as ex:
        text = f'User didn`t find in database'
    await bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: message.from_user.id == int(conf.tg_bot.admin_id), regexp='All users')
async def all_users(message):
    try:
        result = client.get_users()
        text = f'Users: {result}'
    except Exception as ex:
        text = f'User didn`t find in database or didn`t make any operation'
    await bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: message.from_user.id == int(conf.tg_bot.admin_id), regexp='call')
async def caller(message):
    text = f"[INFO] Message from Docker autostart comtainer:\n Bot temporary available now, try it !\n ---press /start or menu---"
    chats =[921610253, 254793128, 269990696, 206508100, 198049052, 738458277, 354907293, 1126904288, 354950537, 336949655, 5359754478]
    for chat in chats:
        await bot.send_message(chat_id=chat, text = text)

   
import asyncio 
def start_polling():
    asyncio.run(bot.infinity_polling())
        
     

