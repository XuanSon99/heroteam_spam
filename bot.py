from telegram import *
from telegram.ext import *
import requests
import json
from types import SimpleNamespace
import math
import random
import time

domain = "https://api.chootc.com"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Xem tỷ giá", url="https://chootc.com"),
                InlineKeyboardButton(
                    text="Mua bán USDT", url="https://exchange.chootc.com"
                ),
            ]
        ]
    )

    buy = requests.get(f"{domain}/api/p2p?type=buy&asset=usdt&fiat=vnd&page=1")
    sell = requests.get(f"{domain}/api/p2p?type=sell&asset=usdt&fiat=vnd&page=1")

    buy_price = buy.json()["data"][19]["adv"]["price"]
    sell_price = sell.json()["data"][19]["adv"]["price"]

    message = f"<b>USDT</b>\nBán: <b>{int(buy_price):,} VND</b>\nMua: <b>{int(sell_price):,} VND</b>"

    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        try:
            if int(time.time()) - item['timestamp'] > 1800:
                await context.bot.delete_message(
                    message_id=item["msg_id"], chat_id=item["group_id"]
                )

                msg = await context.bot.send_message(
                    chat_id=item["group_id"],
                    text=message,
                    parse_mode=constants.ParseMode.HTML,
                    disable_web_page_preview=True,
                    reply_markup=reply_markup 
                )

                item["msg_id"] = msg.message_id
                item["timestamp"] = int(time.time())
                with open("data.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
            else:
                await context.bot.edit_message_text(chat_id=item["group_id"], message_id=item["msg_id"], text=message, parse_mode=constants.ParseMode.HTML,
                    disable_web_page_preview=True)

        except Exception as e:
            print(e)
            if int(time.time()) - item['timestamp'] > 1800:
                msg = await context.bot.send_message(
                    chat_id=item["group_id"],
                    text=message,
                    parse_mode=constants.ParseMode.HTML,
                    disable_web_page_preview=True,
                    reply_markup=reply_markup 
                )

                item["msg_id"] = msg.message_id
                item["timestamp"] = int(time.time())
                with open("data.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
            else:
                await context.bot.edit_message_text(chat_id=item["group_id"], message_id=item["msg_id"], text=message, parse_mode=constants.ParseMode.HTML,
                    disable_web_page_preview=True)


job_queue = app.job_queue

job_minute = job_queue.run_repeating(callback_minute, interval=60, first=10)

app.run_polling()
