import os
import openai
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# دریافت توکن‌ها از متغیرهای محیطی
TELEGRAM_BOT_TOKEN = os.environ["BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_KEY"]
openai.api_key = OPENAI_API_KEY

# تنظیم کیبورد
keyboard = [
    ["آدرس شهرداری", "ساعات کاری شهرداری"],
    ["ثبت شکایت", "شماره تماس"],
    ["نحوه دریافت مجوز ساخت", "خروج"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! به ربات شهرداری نورآباد خوش آمدید.", reply_markup=markup)

# مدیریت پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    responses = {
        "آدرس شهرداری": "نورآباد، میدان اصلی، ساختمان شهرداری.",
        "ساعات کاری شهرداری": "شنبه تا چهارشنبه، ساعت ۸ تا ۱۴.",
        "ثبت شکایت": "لطفاً شکایت خود را تایپ و ارسال کنید.",
        "شماره تماس": "۰۶۶۳۲۵۵۲۲۰۰",
        "نحوه دریافت مجوز ساخت": "برای دریافت مجوز ساخت، به واحد شهرسازی مراجعه فرمایید.",
        "خروج": "خدانگهدار!"
    }

    if text in responses:
        await update.message.reply_text(responses[text])
    else:
        try:
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": text}]
            )
            reply = chat.choices[0].message.content
            await update.message.reply_text(reply)
        except Exception as e:
            await update.message.reply_text("خطایی رخ داد. لطفاً بعداً تلاش کنید.")

# اجرای برنامه
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
