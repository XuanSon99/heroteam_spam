from telegram import *
from telegram.ext import *
import requests
import json
from types import SimpleNamespace
import math
import random

kyc = "👨‍💻 Xác minh KYC"
uytin = "💎 DS Uy tín"

domain = "https://api.chootc.com"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [[KeyboardButton(kyc), KeyboardButton(uytin)]]

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Chào mừng bạn đến với <b>Hero Team</b>",
        parse_mode=constants.ParseMode.HTML,
    )


async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.username
    chat_id = update.effective_chat.id

    print(chat_id)


app = (
    ApplicationBuilder().token("6274365100:AAGi5Mh9fKUNfdOzKUCIH7gauVWfn2Dvy-Y").build()
)

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, messageHandler))


# auto send message
async def callback_minute(context: ContextTypes.DEFAULT_TYPE):
    buy = requests.get(f"{domain}/api/p2p?type=buy&asset=usdt&fiat=vnd&page=1")
    sell = requests.get(f"{domain}/api/p2p?type=sell&asset=usdt&fiat=vnd&page=1")

    # krw_res = requests.get(
    #     f"{domain}/api/rate/bank")

    buy_price = buy.json()["data"][4]["adv"]["price"]
    sell_price = sell.json()["data"][4]["adv"]["price"]

    # krw = krw_res.json()[10]

    # message = f"<b>USDT</b>\nBán: <b>{int(buy_price):,} VND</b>\nMua: <b>{int(sell_price):,} VND</b>\n\n<b>KRW</b>\nBán: <b>{krw['sell']} VND</b>\nMua: <b>{krw['buy']} VND</b>\n\n<b>Liên hệ:</b>\nTelegram: @business1221\nSĐT: 094.797.8888\nXem tỷ giá miễn phí tại: https://chootc.com"

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Xem tỷ giá", url="https://chootc.com"),
                InlineKeyboardButton(text="Mua bán USDT", url="https://exchange.chootc.com"),
            ]
        ]
    )

    message = f"<b>USDT</b>\nBán: <b>{int(buy_price):,} VND</b>\nMua: <b>{int(sell_price):,} VND</b>"

    try:
        baogia1 = requests.get(f"{domain}/api/setup/baogia1")
        baogia2 = requests.get(f"{domain}/api/setup/baogia2")

        last_msg_id = baogia1.json()["value"]
        last_msg_id_2 = baogia2.json()["value"]

        await context.bot.delete_message(
            message_id=last_msg_id, chat_id="-1001871429218"
        )
        msg = await context.bot.send_message(
            chat_id="-1001871429218",
            text=message,
            parse_mode=constants.ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )

        await context.bot.delete_message(
            message_id=last_msg_id_2, chat_id="-1001268866412"
        )
        msg_2 = await context.bot.send_message(
            chat_id="-1001268866412",
            text=message,
            parse_mode=constants.ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )

        requests.put(f"{domain}/api/setup/baogia1", {"value": msg.message_id})
        requests.put(f"{domain}/api/setup/baogia2", {"value": msg_2.message_id})
    except:
        msg = await context.bot.send_message(
            chat_id="-1001871429218",
            text=message,
            parse_mode=constants.ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )
        requests.put(f"{domain}/api/setup/baogia1", {"value": msg.message_id})

        msg_2 = await context.bot.send_message(
            chat_id="-1001268866412",
            text=message,
            parse_mode=constants.ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )
        requests.put(f"{domain}/api/setup/baogia2", {"value": msg_2.message_id})

    # await context.bot.delete_message(message_id=last_msg_id, chat_id='-926818356')
    # msg = await context.bot.send_message(chat_id='-926818356', text=message, parse_mode=constants.ParseMode.HTML)


job_queue = app.job_queue

job_minute = job_queue.run_repeating(callback_minute, interval=3600, first=1)

app.run_polling()
