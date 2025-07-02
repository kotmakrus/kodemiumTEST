import telebot
from telebot import types
from random import *
from time import *

token = 'your token here'
bot = telebot.TeleBot(token)
start_time = time()
animal = ''
animals = {'cat': [1, 50],
           'dog': [1, 50],
           'rabbit': [1, 50],
           'hamster': [1, 50]}


def game_menu():
    return types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton(text='Камень', callback_data='stone')],
        [types.InlineKeyboardButton(text='Ножницы', callback_data='scissors')],
        [types.InlineKeyboardButton(text='Бумага', callback_data='paper')]
    ])


def pet_menu():
    return types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton(text='Кот', callback_data='cat')],
        [types.InlineKeyboardButton(text='Собака', callback_data='dog')],
        [types.InlineKeyboardButton(text='Кролик', callback_data='rabbit')],
        [types.InlineKeyboardButton(text='Хомяк', callback_data='hamster')]
    ])


def action():
    return types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton(text='Покормить', callback_data='feed')],
        [types.InlineKeyboardButton(text='Почесать за ушком', callback_data='ear')],
        [types.InlineKeyboardButton(text='Поиграть', callback_data='play')],
        [types.InlineKeyboardButton(text='Погулять', callback_data='walk')],
        [types.InlineKeyboardButton(text='Ничего не делать', callback_data='nothing')],
        [types.InlineKeyboardButton(text='Переключиться на другого', callback_data='switch')],
        [types.InlineKeyboardButton(text='поиграть в КНБ', callback_data='KNB')]
    ])


def cup():
    return types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton(text='Наругать питомца', callback_data='angry')],
        [types.InlineKeyboardButton(text='Чашка разбилась-на счастье', callback_data='happy')],
    ])


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в игру! Для начала выберите питомца.', reply_markup=pet_menu())


@bot.callback_query_handler(func=lambda call: call.data == 'switch')
def switch(call):
    start(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'KNB')
def KNB(call):
    bot.send_message(call.message.chat.id, 'выберите действие:', reply_markup=game_menu())


@bot.callback_query_handler(func=lambda call: call.data in ('stone', 'scissors', 'paper'))
def GAME(call):
    pet_choice = randint(1, 3)
    if call.data == 'stone':
        if pet_choice == 1:
            bot.send_message(call.message.chat.id, 'ничья', reply_markup=action())
        elif pet_choice == 2:
            bot.send_message(call.message.chat.id, 'вы победили', reply_markup=action())
        elif pet_choice == 3:
            bot.send_message(call.message.chat.id, 'вы проиграли', reply_markup=action())
    elif call.data == 'scissors':
        if pet_choice == 1:
            bot.send_message(call.message.chat.id, 'вы проиграли', reply_markup=action())
        elif pet_choice == 2:
            bot.send_message(call.message.chat.id, 'ничья', reply_markup=action())
        elif pet_choice == 3:
            bot.send_message(call.message.chat.id, 'вы победили', reply_markup=action())
    elif call.data == 'paper':
        if pet_choice == 1:
            bot.send_message(call.message.chat.id, 'вы победили', reply_markup=action())
        elif pet_choice == 2:
            bot.send_message(call.message.chat.id, 'вы проиграли', reply_markup=action())
        elif pet_choice == 3:
            bot.send_message(call.message.chat.id, 'ничья', reply_markup=action())


@bot.callback_query_handler(func=lambda call: call.data in ('cat', 'dog', 'rabbit', 'hamster'))
def choose_pet(call):
    global start_time
    global animal
    animal = call.data
    start_time = time()
    pet = 'Кота' if call.data == 'cat' else 'Пёсика' if call.data == 'dog' else 'Кролика' if call.data == 'rabbit' else 'Хомячка'
    bot.send_message(call.message.chat.id, f'Вывыбрали {pet}! Теперь с питомцем можно взаимодействовать', reply_markup = action())

@bot.callback_query_handler(func = lambda call: call.data in ('feed', 'ear', 'play', 'walk', 'nothing'))
def choose_action(call):
    global start_time
    global animal
    actions = {'feed': [5, 'Вы покормили своего питомца'],
                'ear': [randint(1, 10), 'Вы почесали питомца за ушком'],
               'play': [10, 'Вы поиграли с питомцем'],
               'walk': [15, 'Вы погуляли с питомцем'],
            'nothing': [0,  'Вы ничего не сделали']}
    end = int(time() - start_time)
    start_time = time()
    trouble = randint(1, 5)
    if trouble > 1:
        animals[animal][1] += actions[call.data][0] - end
        if animals[animal][1] < 0:
            animals[animal][1] = 0
        if animals[animal][0] > 1:
            animals[animal][0] -= 1
            animals[animal][1] = 50
        if animals[animal][1] > 100:
            animals[animal][1] = 50
            animals[animal][0] += 1
        #bot.send_photo(call.message.chat.id, open(f'{call.data}/{animal}.jpg', 'rb'))
        bot.send_message(call.message.chat.id, f'{actions[call.data][1]}\nУровень питомца: {animals[animal][0]}\nУровень счастья: {animals[animal][1]}', reply_markup=action())

    else:
        #bot.send_photo(call.message.chat.id, open('cup/cup.jpg', 'rb'))
        bot.send_message(call.message.chat.id,'О нет! Кажется Ваш питомец уронил на пол вашу любимую чашку с чаем и разбил её!\nВаша реакция?', reply_markup=cup())

@bot.callback_query_handler(func=lambda call: call.data in ('angry', 'happy'))
def reaction_2(call):
    if call.data == 'angry':
        animals[animal][1] -= 20
        bot.send_message(call.message.chat.id,f'Вы наругали своегопитомца. Он расстроился(\nУровень питомца: {animals[animal][0]}\nУровень счастья:{animals[animal][1]}', reply_markup = action())
    else:
        animals[animal][1] += 20
        bot.send_message(call.message.chat.id, f'Вы не стали сердится на {animals[animal]}. Он очень обрадовался)\nУровень питомца: {animals[animal][0]}\nУровень счастья: {animals[animal][1]}',reply_markup=action())

bot.infinity_polling()
