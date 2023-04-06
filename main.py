#!/usr/bin/python
# -*- coding: utf8 -*-
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv
import openai
import os
import random

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
# f"Здравствуйте, {username}! Если у вас появились вопросы, мы с удовольствием ответим на них.", f'Привет, {username}! Очень рад, что вы заглянули. Хотите о чем-то узнать?', 'Здравствуйте, давайте помогу вам разобраться', 'Добрый день! Мы оказываем все виды риэлторских и юридических услуг. При обращении в нашу компанию вы получите бесплатную консультацию по возникшему вопросу, и мы не откажем вам в его решении!', "Добрый день. Рад вас видеть!", f'{username},добро пожаловать!'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Приветственное сообщение. `/start`."""
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    text_hello_msg = [
        "Добрый день!👋🏻\nЯ — бот ассистент агентства недвижимости «Колизей». У меня под капотом нейросеть, поэтому вы можете написать вопрос в свободной форме, а я на него отвечу.\n\n"
        "Сейчас я могу ответить на вопросы из следующих категорий: информация, адрес, связь, услуги, оплата, стоимость.\n\n"
        "А если я не буду уверен в ответе — приглашу оператора.😊"
    ]
    rand = random.choice(text_hello_msg)

    logger.info("Пользователь %s начал беседу.", "@" + str(chat_id))

    await context.bot.send_message(chat_id=update.effective_chat.id, text=rand)
    return START_ROUTES


data_send = {
    "информация": [
        "Мы — агентство недвижимости «Колизей», расположенное в Москве, предоставляем комплексные риелторские, брокерские и юридические услуги с 2000 года.\n\n"
        "Официальный сайт агентства недвижимости Колизей позволяет удобно выбирать квартиры, рассчитать через калькулятор и оформить ипотеку онлайн.\n\n"
        "Важное отличие «Колизей» от других риелторских компаний — гарантийный сертификат. В случае проблем мы компенсируем ваши потери по сделке из собственного фонда. Также мало какое агентство по продаже недвижимости может предложить эффективное оформление заявки на ипотеку, а также дополнительные скидки и бонусы. С нами шанс на одобрение ипотеки на 25% выше!"
    ],
    "адрес": [
        "Мы расположены по адресу:\n"
        "📍 Москва, Московский пр-т, 40, оф. 510\n"
        "🕙Офис открыт пн-пт с 09:00 до 18:00, сб с 10:00 до 17:00"
    ],
    "связь": [
        "Вы можете связаться с нами одним из следующих способов:\n"
        "Жилой отдел\n"
        "📞+7 495 111-111\n"
        "Коммерческий отдел\n"
        "📞+7 495 111-111\n"
        "✉️mail@kolizey.ru"
    ],
    "услуги": [
        "Мы предлагаем широкий спектр услуг для наших клиентов:\n"
        "- Юридические,\n"
        "- Выписка из ЕГРП,\n"
        "- Размещение объекта,\n"
        "(Сюда можете выводить любую информацию о ваших услугах)\n\n"
        "С условиями оказания услуг и стоимостью вы можете ознакомиться в прайс листе.",
        "Сбор, оформление, формирование пакетов документов для всех видов сделок и любых операций с недвижимостью:"
        "- Юридические,\n"
        "- Выписка из ЕГРП,\n"
        "- Размещение объекта,\n"
        "(Сюда можете выводить любую информацию о ваших услугах)\n\n"
        "С условиями оказания услуг и стоимостью вы можете ознакомиться в прайс листе.",
    ],
    "оплата": [
        "Для оплаты услуг, воспользуйтесь специальной формой на нашем сайте по ссылке."
    ],
    "оператор": [
        "Пожалуйста, подождите, я переведу ваш вопрос на специалиста.",
        "Сейчас позову оператора",
    ],
    "прощай": [
        "Хорошего дня!",
        "Спасибо за интересную беседу. До встречи!",
        "До встречи!",
        "Спасибо за обращение. До свидания!",
        "Спасибо за обращение. До встречи!",
        "До свидания!",
        "Всего доброго!",
    ],
    "личность": [
        "Я бот ассистент, который помогает пользователям воспользоваться услугами нашего агентства. "
    ],
    "стоимость": [
        "        Стоимость услуг агентства недвижимости «Колизей».\n— *Покупка объекта недвижимости*, 1% от стоимости объекта +39 000 ₽.\n— *Комплексная услуга с гарантией*, 2% от стоимости объекта +39 000 ₽.\n— *Новостройки от застройщика*, 0%.\n— *Новостройки от застройщика с гарантией*, 5% от стоимости объекта.\n— *Юридическое сопровождение сделки*, 39 000 ₽."
    ],
    "неизвестно": [
        "Кажется нам потребуется помощь оператора. Зову?",
        "Извините, но я вас недопонимаю. Позвать оператора?",
        "Пока затрудняюсь вам ответить. Что ж, позвать человека?",
        "Хм, нам непременно нужна помощь оператора, позовем?",
        "Похоже, что без помощи нашего специалиста мы не справимся.",
        "Пожалуйста, перефразируйте свой вопрос или же я могу позвать оператора",
        "Не хочу, чтобы между нами были недопонимания. Перефразируйте свой вопрос или же я могу позвать оператора.",
    ],
    "дела": ["Все хорошо.", "Лучше всех!"],
    "приветствие": [
        f"Здравствуйте! Если у вас появились вопросы, мы с удовольствием ответим на них.",
        f"Привет! Очень рад, что вы заглянули. Хотите о чем-то узнать?",
        "Здравствуйте, давайте помогу вам разобраться",
        "Добрый день! Мы оказываем все виды риэлторских и юридических услуг. При обращении в нашу компанию вы получите бесплатную консультацию по возникшему вопросу, и мы не откажем вам в его решении!",
        "Добрый день. Рад вас видеть!",
    ],
    "график": ["🕙Офис открыт пн-пт с 09:00 до 18:00, сб с 10:00 до 17:00"],
}


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_user = update.message.text
    query = (
        "Привет! Я бот ассистент, который категоризирует вопросы пользователей для дальнейшего ответа из базы знаний. \n"
        "Я знаю следующие категории вопросов: информация о нас - информация, про адрес офиса - адрес, "
        "способах связи с нами - связь, стоимости услуг - стоимость, вариантов услуг - услуги, "
        'как оплатить услуги - оплата. ".\n\n'
        "Вопрос: Кто вы?   \nОтвет: информация\n\n"
        "Вопрос: Как дела?   \nОтвет: дела\n\n"
        "Вопрос: информация   \nОтвет: информация\n\n"
        "Вопрос: расскажи о продукте   \nОтвет: услуги\n\n"
        "Вопрос: Кто ты?   \nОтвет: личность\n\n"
        "Вопрос: Что ты делаешь?   \nОтвет: личность\n\n"
        "Вопрос: Чем вы занимаетесь?   \nОтвет: информация\n\n"
        "Вопрос: Зачем ты?   \nОтвет: личность\n\n"
        "Вопрос: чем ты знаимаешься?   \nОтвет: личность\n\n"
        "Вопрос: Как до вас добраться?   \nОтвет: адрес\n\n"
        "Вопрос: адрес   \nОтвет: адрес\n\n"
        "Вопрос: Где вы?   \nОтвет: адрес\n\n"
        "Вопрос: Сколько вам лет?  \nОтвет: информация\n\n"
        "Вопрос: Позови человека  \nОтвет: оператор\n\n"
        "Вопрос: Оператора позови  \nОтвет: оператор\n\n"
        "Вопрос: Нужен человек  \nОтвет: оператор\n\n"
        "Вопрос: Нужен оператор  \nОтвет: оператор\n\n"
        "Вопрос: человек  \nОтвет: оператор\n\n"
        "Вопрос: оператор  \nОтвет: оператор\n\n"
        "Вопрос: До свидания, прощай, пока  \nОтвет: прощай\n\n"
        "Вопрос: пока  \nОтвет: прощай\n\n"
        "Вопрос: прощай  \nОтвет: прощай\n\n"
        "Вопрос: спасибо за помощь  \nОтвет: прощай\n\n"
        "Вопрос: Спасибо  \nОтвет: прощай\n\n"
        "Вопрос: закончили  \nОтвет: прощай\n\n"
        "Вопрос: до свидания  \nОтвет: прощай\n\n"
        "Вопрос: Как с вами связаться?   \nОтвет: связь\n\n"
        "Вопрос: Хочу позвонить   \nОтвет: связь\n\n"
        "Вопрос: Дай телефон   \nОтвет: связь\n\n"
        "Вопрос: дай почту   \nОтвет: связь\n\n"
        "Вопрос: телефон   \nОтвет: связь\n\n"
        "Вопрос: Связь  \nОтвет: связь\n\n"
        "Вопрос: Какие услуги вы предлагаете?   \nОтвет: услуги\n\n"
        "Вопрос: Сколько стоят ваши услуги?   \nОтвет: стоимость\n\n"
        "Вопрос: Как оплатить услуги?   \nОтвет: оплата\n"
        "Вопрос: Привет   \nОтвет: приветствие\n"
        "Вопрос: здравствуйте   \nОтвет: приветствие\n"
        "Вопрос: Сколько стоят услуги?  \nОтвет: стоимость\n"
        "Вопрос: Стоимость   \nОтвет: стоимость\n"
        "Вопрос: сколько денег нужно?   \nОтвет: стоимость\n"
        "Вопрос: прайс лист  \nОтвет: стоимость\n"
        "Вопрос: график работы  \nОтвет: график\n"
        f"{text_user}\n"
    )

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=query,
            temperature=0,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
    except:
        result = "Прости похоже мои сервера перегружены, пожалуйста попробуй через некоторое время!"

    res = response["choices"][0]["text"].lower()
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=res)
    result = ""
    check = 0
    if "," not in res:
        try:
            for dat in data_send:
                if dat in res:
                    rand = random.choice(data_send[dat])
                    result = result + rand + "\n\n"
            if result == "":
                check = 1
        except:
            check = 1
        if res == "ответ: информация":
            keyboard = [
                [
                    InlineKeyboardButton("Купить/снять", callback_data="0"),
                    InlineKeyboardButton("Официальный сайт", callback_data="1"),
                ],
                [
                    InlineKeyboardButton("Заказать звонок", callback_data="2"),
                    InlineKeyboardButton("Онлайн-консультация", callback_data="3"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=result, reply_markup=reply_markup
            )
            return END_ROUTES

        elif res == "ответ: адрес":
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=result
            )
            await context.bot.send_location(
                chat_id=update.effective_chat.id,
                latitude=55.776861,
                longitude=37.759475,
            )
            return END_ROUTES

        elif res == "ответ: оплата":
            keyboard = [[InlineKeyboardButton("Ссылка на оплату", callback_data="0")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=result, reply_markup=reply_markup
            )
            return END_ROUTES

        elif check == 1:
            rand = random.choice(data_send["неизвестно"])
            result = rand + "\n\n"
            keyboard = [
                [
                    InlineKeyboardButton("Да", callback_data=str(ONE)),
                    InlineKeyboardButton("Нет", callback_data=str(TWO)),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(text=result, reply_markup=reply_markup)
            # await context.bot.send_message(chat_id=update.effective_chat.id, text=result, reply_markup=reply_markup)
            return START_ROUTES

        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=result, parse_mode="Markdown"
            )
            return END_ROUTES
    else:
        try:
            check_info = 0
            check_adress = 0
            check_pay = 0
            for dat in data_send:
                if dat in res:
                    result = ""
                    rand = random.choice(data_send[dat])
                    result = result + rand + "\n\n"
                    if "информация" in res and check_info == 0:
                        keyboard = [
                            [
                                InlineKeyboardButton("Купить/снять", callback_data="0"),
                                InlineKeyboardButton(
                                    "Официальный сайт", callback_data="1"
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    "Заказать звонок", callback_data="2"
                                ),
                                InlineKeyboardButton(
                                    "Онлайн-консультация", callback_data="3"
                                ),
                            ],
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        check_info = 1
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=result,
                            reply_markup=reply_markup,
                        )
                        continue

                    if "адрес" in res and check_adress == 0:
                        check_adress = 1
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id, text=result
                        )
                        await context.bot.send_location(
                            chat_id=update.effective_chat.id,
                            latitude=55.776861,
                            longitude=37.759475,
                        )
                        continue

                    if "оплата" in res and check_pay == 0:
                        keyboard = [
                            [
                                InlineKeyboardButton(
                                    "Ссылка на оплату", callback_data="0"
                                )
                            ]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        check_pay = 1
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=result,
                            reply_markup=reply_markup,
                        )
                        continue

                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=result,
                        parse_mode="Markdown",
                    )

            if result == "":
                check = 1
        except:
            check = 1
        if check == 1:
            rand = random.choice(data_send["неизвестно"])
            result = rand + "\n\n"
            keyboard = [
                [
                    InlineKeyboardButton("Да", callback_data=str(ONE)),
                    InlineKeyboardButton("Нет", callback_data=str(TWO)),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(text=result, reply_markup=reply_markup)
            # await context.bot.send_message(chat_id=update.effective_chat.id, text=result, reply_markup=reply_markup)
            return START_ROUTES


async def voice_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_voice = "Извините, я немогу прослушать голосовое, напишите пожалуйста текстом!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_voice)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_command = (
        "Вы хотели что то спросить?\n"
        "Задайте вопрос точнее и я постараюсь на него ответить."
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_command)


async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.callback_query.message.text

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=msg)
    rand = random.choice(data_send["оператор"])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=rand)


async def not_helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.callback_query.message.text

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=msg)
    text_command = "Хорошо, пожалуйста, перефразируйте свой вопрос\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_command)


def main() -> None:
    """Запустить бота."""
    # Создайте приложение и передайте ему токен вашего бота.
    application = Application.builder().token(token_bot_tg).build()

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    unknown_handler = MessageHandler(filters.COMMAND, unknown_command)
    voice_msg_handler = MessageHandler(filters.VOICE, voice_msg)
    # start_handler = CommandHandler('start', start)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(helper, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(not_helper, pattern="^" + str(TWO) + "$"),
            ],
            END_ROUTES: [
                CallbackQueryHandler(unknown_command, pattern="^" + str(ONE) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    # application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(unknown_handler)
    application.add_handler(voice_msg_handler)

    application.run_polling()


if __name__ == "__main__":
    # Объявление глобальных переменных.
    load_dotenv()

    START_ROUTES, END_ROUTES, TYPE_REPLY = range(3)
    # Параметры обратного вызова
    ONE, TWO = range(2)

    openai.api_key = os.environ.get("openai_apikey")
    token_bot_tg = os.environ.get("token_bot_tg")

    main()
