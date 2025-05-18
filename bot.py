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
    ["ثبت شکایت", "شماره تماس"],
    ["نحوه دریافت مجوز ساخت", "خروج"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! به ربات شهرداری نورآباد خوش آمدید.", reply_markup=markup
    )

# پاسخ به پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    predefined_responses = {
        "آدرس شهرداری": "نورآباد، میدان اصلی، ساختمان شهرداری.",
        "ساعات کاری شهرداری": "شنبه تا چهارشنبه، ساعت ۸ تا ۱۴.",
        "ثبت شکایت": "لطفاً شکایت خود را تایپ و ارسال کنید.",
        "شماره تماس": "۰۶۶۳۲۵۵۲۲۰۰",
        "نحوه دریافت مجوز ساخت": "برای دریافت مجوز ساخت، به واحد شهرسازی مراجعه فرمایید.",
        "خروج": "خدانگهدار!"
    }

    if text in predefined_responses:
        await update.message.reply_text(predefined_responses[text])
    else:
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": text}]
            )
            reply = response.choices[0].message.content
            await update.message.reply_text(reply)
        except Exception as e:
            print("خطا:", e)
            await update.message.reply_text("خطایی رخ داد. لطفاً بعداً تلاش کنید.")

# اجرای برنامه
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
