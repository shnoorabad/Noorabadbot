import os
import openai
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

# کلید API
openai.api_key = os.getenv("OPENAI_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")

# کیبورد ساده
keyboard = [
    ["آدرس شهرداری", "ساعات کاری شهرداری"],
    ["درباره ما", "شماره تماس"],
    ["نحوه دریافت مجوز ساخت", "خروج"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! به ربات شهرداری نورآباد خوش آمدید.", reply_markup=markup
    )

# مدیریت پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    responses = {
        "آدرس شهرداری": "نورآباد، خیابان کشاورز ، ساختمان شهرداری.",
        "ساعات کاری شهرداری": "شنبه تا چهارشنبه، ساعت ۸ تا ۱۴.",
        "درباره ما": "سرپست شهرداری؛ محمد مرادپور ،تهیه وتدوین ربات : علی معصومی پور.",
        "شماره تماس": "۰۶۶۳۲۷۲۴۰۵۷-۸",
        "نحوه دریافت مجوز ساخت": "برای دریافت مجوز ساخت، به واحد ساختمانی مراجعه فرمایید.",
        "خروج": "خدانگهدار!"
    }

    if text in responses:
        await update.message.reply_text(responses[text])
    else:
        try:
            chat = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "شما یک ربات پاسخگوی شهرداری نورآباد هستید. شهردار فعلی نورآباد علی نجات نورعلی است. به سوالات مردم درباره شهرداری پاسخ بده."},
                    {"role": "user", "content": text}
                ]
            )
            reply = chat.choices[0].message.content
            await update.message.reply_text(reply)
        except Exception as e:
            await update.message.reply_text("خطایی رخ داد. لطفاً بعداً تلاش کنید.")
