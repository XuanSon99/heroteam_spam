from telegram import *
from telegram.ext import *
import requests
import json
from types import SimpleNamespace
import math
import random

kyc = "👨‍💻 Xác minh KYC"
uytin = "💎 DS Uy tín"

domain = "https://chootc.com"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [[KeyboardButton(kyc), KeyboardButton(uytin)]]

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Chào mừng bạn đến với <b>Hero Team</b>", parse_mode=constants.ParseMode.HTML)


async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.username
    chat_id = update.effective_chat.id

app = ApplicationBuilder().token(
    "6274365100:AAGi5Mh9fKUNfdOzKUCIH7gauVWfn2Dvy-Y").build()

app.add_handler(CommandHandler("start", start)) 
app.add_handler(MessageHandler(filters.ALL, messageHandler))


# auto send message
async def callback_minute(context: ContextTypes.DEFAULT_TYPE):

    buy = requests.get(
        f"{domain}/api/p2p?type=buy&asset=usdt&fiat=vnd&page=1")
    sell = requests.get(
        f"{domain}/api/p2p?type=sell&asset=usdt&fiat=vnd&page=1")

    krw_res = requests.get(
        f"{domain}/api/rate/bank")

    buy_price = buy.json()['data'][4]['adv']['price']
    sell_price = sell.json()['data'][4]['adv']['price']

    krw = krw_res.json()[10]

    message = f"<b>USDT</b>\nBán: <b>{int(buy_price):,} VND</b>\nMua: <b>{int(sell_price):,} VND</b>\n\n<b>KRW</b>\nBán: <b>{krw['sell']} VND</b>\nMua: <b>{krw['buy']} VND</b>\n\nXem tỷ giá miễn phí tại:\nhttps://chootc.com"

    try:
        res = requests.get(f"{domain}/api/setup")
        last_msg_id = res.json()[0]["value"]
        
        await context.bot.delete_message(message_id=last_msg_id, chat_id='-1001871429218')
        msg = await context.bot.send_message(chat_id='-1001871429218', text=message, parse_mode=constants.ParseMode.HTML, link_preview=False)

        requests.put(
        f"{domain}/api/setup/1", {'value': msg.message_id})
    except:
        msg = await context.bot.send_message(chat_id='-1001871429218', text=message, parse_mode=constants.ParseMode.HTML, link_preview=False)
        
        requests.put(
        f"{domain}/api/setup/1", {'value': msg.message_id})

    # await context.bot.delete_message(message_id=last_msg_id, chat_id='-926818356')
    # msg = await context.bot.send_message(chat_id='-926818356', text=message, parse_mode=constants.ParseMode.HTML)


job_queue = app.job_queue

job_minute = job_queue.run_repeating(callback_minute, interval=3600, first=1)

app.run_polling()